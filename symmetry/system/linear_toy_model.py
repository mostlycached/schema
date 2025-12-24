"""
Linear Toy Model for the Creative Process

Implements the framework from PROCESS.md §6:
- World space W = ℝⁿ
- Perception space P = ℝᵏ (k < n)
- Action space A = ℝᵐ (m ≤ n)

The creative loop: w_{t+1} = w_t + E @ N @ M @ w_t = (I + L) @ w_t
where L = E @ N @ M

This module allows exploration of:
- Convergence vs. oscillation vs. divergence regimes
- Symmetry-breaking measurement
- The perception-action gap

Usage:
    python linear_toy_model.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class CreativeLoop:
    """
    Encapsulates the perception-action-transition structure.
    
    M: Perception matrix (k × n) - projects world to percepts
    N: Policy matrix (m × k) - maps percepts to actions  
    E: Embedding matrix (n × m) - embeds actions into world
    """
    M: np.ndarray  # k × n (perception)
    N: np.ndarray  # m × k (policy)
    E: np.ndarray  # n × m (embedding)
    noise_scale: float = 0.0
    
    def __post_init__(self):
        self.n = self.M.shape[1]  # world dim
        self.k = self.M.shape[0]  # perception dim
        self.m = self.N.shape[0]  # action dim
        
        # Validate dimensions
        assert self.N.shape[1] == self.k, f"N should be {self.m}×{self.k}"
        assert self.E.shape == (self.n, self.m), f"E should be {self.n}×{self.m}"
        
        # Compute L = E @ N @ M
        self.L = self.E @ self.N @ self.M
        
    @property
    def dynamics_matrix(self) -> np.ndarray:
        """The full dynamics matrix I + L"""
        return np.eye(self.n) + self.L
    
    def step(self, w: np.ndarray) -> np.ndarray:
        """Single step of the creative loop."""
        p = self.M @ w                    # perceive
        a = self.N @ p                    # decide
        delta = self.E @ a                # act
        noise = self.noise_scale * np.random.randn(self.n) if self.noise_scale > 0 else 0
        return w + delta + noise
    
    def run(self, w0: np.ndarray, steps: int) -> np.ndarray:
        """Run the loop for multiple steps. Returns trajectory (steps+1 × n)."""
        trajectory = np.zeros((steps + 1, self.n))
        trajectory[0] = w0
        w = w0.copy()
        for t in range(steps):
            w = self.step(w)
            trajectory[t + 1] = w
        return trajectory
    
    def eigenanalysis(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Analyze eigenvalues of the dynamics matrix.
        
        Returns:
            eigenvalues: Complex eigenvalues of (I + L)
            eigenvectors: Corresponding eigenvectors
        """
        return np.linalg.eig(self.dynamics_matrix)
    
    def regime(self) -> str:
        """Classify the dynamical regime based on eigenvalues."""
        eigenvalues, _ = self.eigenanalysis()
        max_abs = np.max(np.abs(eigenvalues))
        has_complex = np.any(np.abs(np.imag(eigenvalues)) > 1e-10)
        
        if max_abs < 1 - 1e-10:
            return "convergent" + (" (oscillating)" if has_complex else " (monotonic)")
        elif max_abs > 1 + 1e-10:
            return "divergent" + (" (oscillating)" if has_complex else " (monotonic)")
        else:
            return "critical" + (" (oscillating)" if has_complex else " (fixed)")
    
    def bottleneck_rank(self) -> int:
        """The rank bottleneck: min(k, m)"""
        return min(self.k, self.m)
    
    def effective_rank_L(self) -> int:
        """The actual rank of L (may be less than bottleneck)."""
        return np.linalg.matrix_rank(self.L)


def equivariance_error(L: np.ndarray, group_reps: List[np.ndarray]) -> float:
    """
    Measure how much L breaks symmetry with respect to a group.
    
    Args:
        L: The dynamics matrix (n × n)
        group_reps: List of matrix representations ρ(g) for group elements g
        
    Returns:
        Average squared Frobenius norm of [L, ρ(g)] = Lρ(g) - ρ(g)L
    """
    errors = []
    for rho_g in group_reps:
        commutator = L @ rho_g - rho_g @ L
        errors.append(np.linalg.norm(commutator, 'fro') ** 2)
    return np.mean(errors)


def d4_representations(n: int) -> List[np.ndarray]:
    """
    Generate D₄ (dihedral group of square) representations on ℝⁿ.
    Assumes n ≥ 2 and acts on first two coordinates.
    
    Returns 8 matrices: {e, r, r², r³, s, sr, sr², sr³}
    """
    reps = []
    
    # Rotation by 90° in first two coords
    def rot90():
        R = np.eye(n)
        R[0, 0], R[0, 1], R[1, 0], R[1, 1] = 0, -1, 1, 0
        return R
    
    # Reflection across first axis
    def reflect():
        S = np.eye(n)
        S[1, 1] = -1
        return S
    
    r = rot90()
    s = reflect()
    e = np.eye(n)
    
    # Generate all 8 elements
    reps.append(e)                          # e
    reps.append(r)                          # r
    reps.append(r @ r)                      # r²
    reps.append(r @ r @ r)                  # r³
    reps.append(s)                          # s
    reps.append(s @ r)                      # sr
    reps.append(s @ r @ r)                  # sr²
    reps.append(s @ r @ r @ r)              # sr³
    
    return reps


# ============================================================================
# Information Geometry (from PROCESS.md §16)
# ============================================================================

def fisher_information(M: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """
    Compute Fisher information matrix for linear perception map.
    
    For φ(w) = Mw with Gaussian noise N(0, σ²I), the Fisher information is:
        F = (1/σ²) M @ M^T
    
    This is a k×k matrix measuring distinguishability in perception space.
    
    Args:
        M: Perception matrix (k × n)
        sigma: Noise standard deviation
        
    Returns:
        F: Fisher information matrix (k × k)
    """
    return (1 / sigma**2) * M @ M.T


def natural_gradient(grad_V: np.ndarray, F: np.ndarray, regularization: float = 1e-6) -> np.ndarray:
    """
    Compute natural gradient by adjusting for Fisher metric.
    
    ∇̃V = F^{-1} ∇V
    
    Args:
        grad_V: Standard gradient in perception space (k,)
        F: Fisher information matrix (k × k)
        regularization: Small value for numerical stability
        
    Returns:
        Natural gradient (k,)
    """
    F_reg = F + regularization * np.eye(F.shape[0])
    return np.linalg.solve(F_reg, grad_V)


def mutual_information_linear(M: np.ndarray, sigma: float = 1.0, 
                               prior_cov: Optional[np.ndarray] = None) -> float:
    """
    Compute mutual information I(W; P) for linear Gaussian model.
    
    I(W; P) = (1/2) log det(I + (1/σ²) M^T @ M @ Σ_w)
    
    where Σ_w is the prior covariance on W.
    
    Args:
        M: Perception matrix (k × n)
        sigma: Noise standard deviation
        prior_cov: Prior covariance on W (n × n), defaults to identity
        
    Returns:
        Mutual information in nats
    """
    n = M.shape[1]
    if prior_cov is None:
        prior_cov = np.eye(n)
    
    inner = np.eye(n) + (1 / sigma**2) * M.T @ M @ prior_cov
    return 0.5 * np.log(np.linalg.det(inner))


def fisher_value(M: np.ndarray, w: np.ndarray, sigma: float = 1.0) -> float:
    """
    Compute log-det-Fisher value function at a point.
    
    V_Fisher(w) = log det F(φ(w))
    
    For linear case, this is constant (doesn't depend on w).
    But we include it for interface consistency with nonlinear extensions.
    
    Args:
        M: Perception matrix
        w: World state
        sigma: Noise scale
        
    Returns:
        Log-determinant of Fisher information
    """
    F = fisher_information(M, sigma)
    return np.log(np.linalg.det(F) + 1e-10)


class InfoGeomCreativeLoop(CreativeLoop):
    """
    Creative loop extended with information-geometric awareness.
    
    Uses natural gradient instead of standard gradient when computing
    the perception-to-action mapping.
    """
    
    def __init__(self, M: np.ndarray, N: np.ndarray, E: np.ndarray, 
                 sigma: float = 1.0, noise_scale: float = 0.0):
        super().__init__(M, N, E, noise_scale)
        self.sigma = sigma
        self._F = fisher_information(M, sigma)
        
    @property
    def fisher(self) -> np.ndarray:
        """Fisher information matrix for perception space."""
        return self._F
    
    def mutual_info(self) -> float:
        """Mutual information I(W; P)."""
        return mutual_information_linear(self.M, self.sigma)
    
    def step_natural(self, w: np.ndarray, target_p: np.ndarray) -> np.ndarray:
        """
        Step using natural gradient toward target percept.
        
        Instead of w_{t+1} = w_t + E @ N @ M @ w_t,
        we use: w_{t+1} = w_t + E @ F^{-1} @ (target_p - M @ w_t)
        
        This accounts for the geometry of perception space.
        """
        p = self.M @ w
        grad_V = target_p - p  # Gradient of ||p - target||²
        nat_grad = natural_gradient(grad_V, self._F)
        delta = self.E @ nat_grad[:self.m]  # Project to action dim
        return w + delta


def example_info_geometry():
    """Demonstrate information geometry concepts."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Information Geometry")
    print("="*60)
    
    n, k, m = 4, 2, 2
    
    # Create a perception map with different sensitivities
    M = np.array([[1.0, 0.2, 0, 0], 
                  [0, 0, 0.3, 1.0]])
    
    # Different noise levels
    for sigma in [0.1, 1.0, 10.0]:
        F = fisher_information(M, sigma)
        mi = mutual_information_linear(M, sigma)
        print(f"\nσ = {sigma}:")
        print(f"  Fisher det: {np.linalg.det(F):.4f}")
        print(f"  Mutual info: {mi:.4f} nats")
        print(f"  Fisher eigenvalues: {np.linalg.eigvalsh(F).round(3)}")
    
    # Compare standard vs natural gradient
    print("\n--- Standard vs Natural Gradient ---")
    grad = np.array([1.0, 0.0])  # Gradient purely in dim 0
    F = fisher_information(M, sigma=1.0)
    nat = natural_gradient(grad, F)
    print(f"Standard gradient: {grad}")
    print(f"Natural gradient:  {nat.round(4)}")
    print(f"Fisher metric:\n{F.round(4)}")



# ============================================================================
# Visualization
# ============================================================================

def plot_eigenvalues(loop: CreativeLoop, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Plot eigenvalues in the complex plane with unit circle."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    
    eigenvalues, _ = loop.eigenanalysis()
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Unit circle')
    
    # Eigenvalues
    ax.scatter(np.real(eigenvalues), np.imag(eigenvalues), 
               s=100, c='crimson', zorder=5, label='Eigenvalues')
    
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title(f'Eigenvalues of (I + L)\nRegime: {loop.regime()}')
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def plot_trajectory_2d(trajectory: np.ndarray, dims: Tuple[int, int] = (0, 1),
                       ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Plot trajectory projected onto two dimensions."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    d1, d2 = dims
    x, y = trajectory[:, d1], trajectory[:, d2]
    
    # Color by time
    colors = np.linspace(0, 1, len(x))
    scatter = ax.scatter(x, y, c=colors, cmap='viridis', s=30)
    ax.plot(x, y, 'k-', alpha=0.3, linewidth=0.5)
    
    # Mark start and end
    ax.scatter([x[0]], [y[0]], s=200, c='green', marker='o', zorder=5, label='Start')
    ax.scatter([x[-1]], [y[-1]], s=200, c='red', marker='x', zorder=5, label='End')
    
    ax.set_xlabel(f'Dimension {d1}')
    ax.set_ylabel(f'Dimension {d2}')
    ax.set_title('Creative Trajectory')
    ax.legend()
    plt.colorbar(scatter, ax=ax, label='Time')
    
    return ax


def plot_symmetry_breaking_sweep(n: int = 4, k: int = 2, m: int = 2, 
                                  num_samples: int = 50) -> plt.Figure:
    """
    Sweep over random matrices and measure symmetry-breaking vs. spectral radius.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    d4_reps = d4_representations(n)
    
    spectral_radii = []
    equiv_errors = []
    regimes = []
    
    for _ in range(num_samples):
        # Random matrices with controlled scale
        scale = np.random.uniform(0.1, 0.5)
        M = np.random.randn(k, n) * scale
        N = np.random.randn(m, k) * scale
        E = np.random.randn(n, m) * scale
        
        loop = CreativeLoop(M, N, E)
        eigenvalues, _ = loop.eigenanalysis()
        
        spectral_radii.append(np.max(np.abs(eigenvalues)))
        equiv_errors.append(equivariance_error(loop.L, d4_reps))
        regimes.append(loop.regime())
    
    # Plot 1: Spectral radius histogram
    axes[0].hist(spectral_radii, bins=20, edgecolor='black', alpha=0.7)
    axes[0].axvline(1, color='red', linestyle='--', label='Criticality')
    axes[0].set_xlabel('Spectral Radius of (I + L)')
    axes[0].set_ylabel('Count')
    axes[0].set_title('Distribution of Dynamical Regimes')
    axes[0].legend()
    
    # Plot 2: Symmetry-breaking vs spectral radius
    axes[1].scatter(equiv_errors, spectral_radii, alpha=0.6)
    axes[1].axhline(1, color='red', linestyle='--', alpha=0.5)
    axes[1].set_xlabel('Equivariance Error (D₄ symmetry-breaking)')
    axes[1].set_ylabel('Spectral Radius')
    axes[1].set_title('Symmetry-Breaking vs. Dynamics')
    
    plt.tight_layout()
    return fig


# ============================================================================
# Example Runs
# ============================================================================

def example_convergent():
    """A system that converges: all eigenvalues inside unit circle."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Convergent System")
    print("="*60)
    
    n, k, m = 4, 2, 2
    
    # Small matrices → eigenvalues near 1
    M = 0.1 * np.array([[1, 0, 0.5, 0], [0, 1, 0, 0.5]])
    N = 0.2 * np.array([[1, 0.3], [0.3, 1]])
    E = 0.1 * np.array([[1, 0], [0, 1], [0.5, 0], [0, 0.5]])
    
    loop = CreativeLoop(M, N, E)
    
    print(f"Dimensions: W=ℝ{n}, P=ℝ{k}, A=ℝ{m}")
    print(f"Bottleneck rank: {loop.bottleneck_rank()}")
    print(f"Effective rank of L: {loop.effective_rank_L()}")
    print(f"Regime: {loop.regime()}")
    
    eigenvalues, _ = loop.eigenanalysis()
    print(f"Eigenvalues of (I + L): {eigenvalues.round(3)}")
    print(f"Spectral radius: {np.max(np.abs(eigenvalues)):.3f}")
    
    # Run trajectory
    w0 = np.array([1.0, 0.5, -0.3, 0.2])
    trajectory = loop.run(w0, steps=50)
    print(f"Initial: {w0}")
    print(f"Final:   {trajectory[-1].round(4)}")
    
    return loop, trajectory


def example_oscillating():
    """A system with complex eigenvalues: spiraling dynamics."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Oscillating System")
    print("="*60)
    
    n, k, m = 4, 2, 2
    
    # Rotation-inducing structure
    M = 0.15 * np.array([[1, 0.5, 0, 0], [0, 0, 1, 0.5]])
    N = 0.3 * np.array([[0, -1], [1, 0]])  # 90° rotation in action space
    E = 0.15 * np.array([[1, 0], [0, 1], [0.3, 0], [0, 0.3]])
    
    loop = CreativeLoop(M, N, E)
    
    print(f"Regime: {loop.regime()}")
    eigenvalues, _ = loop.eigenanalysis()
    print(f"Eigenvalues: {eigenvalues.round(3)}")
    
    w0 = np.array([1.0, 0.0, 0.5, 0.0])
    trajectory = loop.run(w0, steps=100)
    
    return loop, trajectory


def example_symmetry_breaking():
    """Demonstrate symmetry-breaking measurement."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Symmetry-Breaking Analysis")
    print("="*60)
    
    n = 4
    d4_reps = d4_representations(n)
    
    # Case A: D₄-equivariant L (acts only on dims 2,3, leaving 0,1 to D₄)
    L_symmetric = np.zeros((n, n))
    L_symmetric[2, 2] = 0.1
    L_symmetric[3, 3] = 0.1
    
    # Case B: Non-equivariant L (mixes all dimensions)
    np.random.seed(42)
    L_asymmetric = 0.1 * np.random.randn(n, n)
    
    err_sym = equivariance_error(L_symmetric, d4_reps)
    err_asym = equivariance_error(L_asymmetric, d4_reps)
    
    print(f"Equivariance error (symmetric L):  {err_sym:.6f}")
    print(f"Equivariance error (asymmetric L): {err_asym:.6f}")
    print(f"Ratio: {err_asym / (err_sym + 1e-10):.1f}x more symmetry-breaking")


def main():
    """Run all examples and generate visualizations."""
    print("Creative Loop: Linear Toy Model")
    print("From PROCESS.md §6")
    
    # Run examples
    loop1, traj1 = example_convergent()
    loop2, traj2 = example_oscillating()
    example_symmetry_breaking()
    example_info_geometry()
    
    # Generate plots
    print("\n" + "="*60)
    print("Generating visualizations...")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    plot_eigenvalues(loop1, axes[0, 0])
    axes[0, 0].set_title(f'Convergent System\n{loop1.regime()}')
    
    plot_eigenvalues(loop2, axes[0, 1])
    axes[0, 1].set_title(f'Oscillating System\n{loop2.regime()}')
    
    # Trajectory plots (for 2D projection)
    colors1 = np.linspace(0, 1, len(traj1))
    axes[1, 0].scatter(traj1[:, 0], traj1[:, 1], c=colors1, cmap='viridis', s=20)
    axes[1, 0].plot(traj1[:, 0], traj1[:, 1], 'k-', alpha=0.2)
    axes[1, 0].scatter([traj1[0, 0]], [traj1[0, 1]], s=150, c='green', marker='o', zorder=5)
    axes[1, 0].scatter([traj1[-1, 0]], [traj1[-1, 1]], s=150, c='red', marker='x', zorder=5)
    axes[1, 0].set_xlabel('Dim 0')
    axes[1, 0].set_ylabel('Dim 1')
    axes[1, 0].set_title('Convergent Trajectory')
    
    colors2 = np.linspace(0, 1, len(traj2))
    axes[1, 1].scatter(traj2[:, 0], traj2[:, 1], c=colors2, cmap='viridis', s=20)
    axes[1, 1].plot(traj2[:, 0], traj2[:, 1], 'k-', alpha=0.2)
    axes[1, 1].scatter([traj2[0, 0]], [traj2[0, 1]], s=150, c='green', marker='o', zorder=5)
    axes[1, 1].scatter([traj2[-1, 0]], [traj2[-1, 1]], s=150, c='red', marker='x', zorder=5)
    axes[1, 1].set_xlabel('Dim 0')
    axes[1, 1].set_ylabel('Dim 1')
    axes[1, 1].set_title('Oscillating Trajectory')
    
    plt.tight_layout()
    plt.savefig('creative_loop_analysis.png', dpi=150)
    print("Saved: creative_loop_analysis.png")
    
    # Symmetry sweep
    fig2 = plot_symmetry_breaking_sweep(n=4, k=2, m=2, num_samples=100)
    plt.savefig('symmetry_breaking_sweep.png', dpi=150)
    print("Saved: symmetry_breaking_sweep.png")
    
    print("\nDone! Plots saved to current directory.")


if __name__ == "__main__":
    main()
