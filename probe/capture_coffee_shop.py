#!/usr/bin/env python3
"""
Scene extracted from coffee shop images - Morning at the Coffee Shop
Generated from visual analysis of the space and atmosphere.
"""

from memoir_manager import MemoirRepo
from datetime import datetime
import uuid

# Scene extracted from images
scene_data = {
    "scene_id": str(uuid.uuid4()),
    "title": "Morning at the Coffee Shop",
    "date": "2025-12-10",  # Today's date based on image capture
    "location": "Urban coffee shop with botanical interior",
    "duration": "1-2 hours",
    "tags": ["coffee", "morning", "urban", "solitude", "reading", "public space"],
    
    "phenomenology": {
        "cognitive_style": {
            "time_experience": "Suspended - time slows in the warm light and plant-filtered space",
            "space_experience": "Layered - tropical plants create pockets within the larger room; intimate despite being public",
            "attention_mode": "Diffuse awareness - observing the room while focused on books/thoughts; peripheral awareness of conversations"
        },
        "intersubjectivity": {
            "shared_meanings": [
                "Coffee shop as third place - neither home nor work",
                "Laptop/book on table claims territory",
                "Don't disturb someone with headphones",
                "Morning regulars recognize each other without speaking"
            ],
            "emotional_tone": "Contemplative calm with undercurrent of productivity; gentle morning energy",
            "intimacy_level": "Anonymous co-presence - surrounded by strangers but comfortable; occasional eye contact with barista"
        },
        "body_experience": {
            "sensations": [
                "Warmth of coffee cup in hands",
                "Hard wooden chair against back",
                "Cool morning air when door opens",
                "Aroma of espresso and baked goods",
                "Soft ambient music blending with conversation hum"
            ],
            "posture": "Seated at wooden table, slightly leaning forward over books/papers; beanie on for warmth",
            "mobility": "Stationary for extended period; occasional walk to counter or restroom"
        }
    },
    
    "structure": {
        "capital": {
            "economic": "Cost of coffee (~$5-7) as price of admission to the space; laptop/books signal intellectual work",
            "cultural": "Knowing how to order; appreciation for 'third wave' coffee aesthetics; reading dense academic texts signals cultural capital",
            "social": "Regularity creates recognition; being comfortable alone in public",
            "symbolic": "The urban creative/intellectual at work; books on table (including what appears to be design/theory texts) as identity marker"
        },
        "doxa": {
            "beliefs": [
                "Good coffee shops should feel like a living room",
                "It's acceptable to occupy space for hours if you buy something",
                "Morning is the best time for focused work in public",
                "Plants make spaces better"
            ],
            "taboos": [
                "Being too loud on phone calls",
                "Not buying anything",
                "Staring at other patrons",
                "Sitting at a large table alone during rush hour"
            ]
        },
        "habitus": {
            "behaviors": [
                "Claiming a table with belongings before ordering",
                "Nodding at barista upon entry",
                "Checking phone intermittently",
                "Taking photo of the space/moment",
                "Organizing papers and books ritually"
            ],
            "gestures": [
                "Careful sipping to avoid spills on books",
                "Adjusting beanie",
                "Glancing up to people-watch between reading",
                "Mouse/trackpad movements"
            ],
            "language_style": "Brief, friendly exchanges with barista; internal monologue while reading; code-switching between academic text and ambient observation"
        },
        "hierarchy": {
            "position": "Customer/patron - temporary claim to space; regular (based on comfort level); adult with autonomy",
            "mobility": "Free to come and go; choosing this space over others; economic barrier is low but present"
        }
    },
    
    "system": {
        "function": {
            "primary": "Third place - transition space between home and other obligations; venue for solo intellectual work",
            "secondary": [
                "Social observation", 
                "Caffeination ritual",
                "Escape from domestic/work environments",
                "Performance of intellectual identity"
            ]
        },
        "binary_code": {
            "code": "customer/staff; present/absent; focused/distracted",
            "position": "Customer who is present and focused"
        },
        "boundaries": {
            "entry_criteria": [
                "Willingness to purchase",
                "Knowledge of coffee shop norms",
                "Being dressed for public",
                "Morning hours (before afternoon crowd)"
            ],
            "exit_criteria": [
                "Coffee finished and lingering feels awkward",
                "Space gets too crowded/loud",
                "Next appointment/obligation",
                "Laptop battery dies"
            ]
        },
        "communication": {
            "medium": "Transactional (ordering), visual (menu boards, aesthetic cues), ambient (music, conversation murmur)",
            "code_switching": [
                "Professional/academic reading → people watching",
                "Internal thought → brief spoken order",
                "Focused work → phone scrolling breaks"
            ]
        }
    },
    
    "inhabitants": [
        {
            "role": "Self as patron/intellectual worker",
            "relationship": "Primary actor",
            "power": "Customer autonomy within commercial space",
            "name": ""
        },
        {
            "role": "Barista",
            "relationship": "Service provider; friendly but professional",
            "power": "Controls access to coffee and implicitly regulates space",
            "name": ""
        },
        {
            "role": "Other patrons",
            "relationship": "Anonymous co-inhabitants of third place",
            "power": "Equal customers; mutual unspoken agreement to share space respectfully",
            "name": ""
        },
        {
            "role": "The space itself",
            "relationship": "Container and atmosphere-generator",
            "power": "Shapes behavior through design (plants creating intimacy, wood warmth, yellow tile creating visual rhythm)",
            "name": ""
        },
        {
            "role": "The books/papers",
            "relationship": "Props and genuine tools; markers of intent",
            "power": "Justify presence; create focused bubble",
            "name": ""
        }
    ],
    
    "genealogy": {
        "origin": "Third wave coffee culture (2000s+); gentrification of urban neighborhoods; remote work normalization; coffee house tradition dating to 17th century",
        "influences": [
            "Instagram aesthetic culture (plants, design, lighting)",
            "Post-pandemic return to public spaces",
            "Academic/creative work culture requiring 'focus spaces'",
            "Urban density creating need for third places"
        ]
    },
    
    "tension": {
        "internal": "Desire for solitude vs. need for ambient human presence; productive work vs. meditative observation",
        "external": "Commercial space requiring purchase for legitimacy; gentrification pricing out original neighborhood; balance between work focus and social awareness",
        "trajectory": "Growth/mutation - this third place culture continues to evolve with remote work; decay threatens as rents rise"
    },
    
    "narrative": {
        "description": """Arrived mid-morning. The coffee shop glows with natural light filtered through massive fiddle-leaf fig trees. Yellow and white geometric floor tiles create a rhythm underfoot. Ordered at the counter - brief exchange with the barista who seems to recognize me. 

Claimed a wooden table beneath the botanical canopy. Books spread out: design theory, phenomenology texts. A beer glass (La Nacion) repurposed as water vessel. White mouse sits idle beside papers covered in pink and blue diagrams.

Two women conversed nearby, one in a black vest holding something orange (pastry? vitamin drink?), another in striped sweater and blue beanie. Their voices formed part of the ambient texture. An older man in grey sat alone near the counter, reading.

The space feels like a terrarium - enclosed but breathing. Bentwood chairs, exposed wood beams, white brick. I took a selfie outside before entering: grey sweater, beanie, on a city street with buses passing. Dunkin' sign visible across the way. The transition from cold street to warm interior was marked.

Time moved differently here. Sipped coffee. Read. Watched. Thought. The plants seemed to create private pockets even in this shared room. This is a world unto itself - temporary, renewable, necessary.""",
        
        "key_moments": [
            "First sip of coffee after ordering - the ritual begins",
            "Looking up from reading to notice the light through plants",
            "Making eye contact with another patron",
            "Taking the selfie outside before entering - documenting the threshold",
            "Arranging books and papers into productive configuration"
        ],
        "turning_points": [
            "Deciding to come here instead of working from home",
            "The moment the space shifts from 'entering' to 'inhabited'"
        ]
    },
    
    "reflection": {
        "significance": "This coffee shop represents a constructed third place in urban life - the attempt to create intimate public space. It's where I perform intellectual identity while genuinely working. The botanical excess creates 'nature' within capital. This scene captures the ambivalence of late-capitalist urban dwelling: paying for the right to exist comfortably in public, yet genuinely finding solace there.",
        
        "patterns": [
            "Repeat visits to same coffee shops - seeking familiarity",
            "Morning as sacred time for this kind of work",
            "Books as both tools and identity markers",
            "Photography of the space - documenting/memorializing the temporary",
            "Oscillation between focus and observation"
        ],
        
        "questions": [
            "Why does working in public feel more legitimate than working at home?",
            "What does this pattern of seeking third places reveal about home and work as insufficient?",
            "How much of this is performance vs. genuine need?",
            "What does it mean that I photograph this moment - for whom?",
            "Is this coffee shop a pocket of resistance or just boutique capitalism?",
            "How does the botanical excess relate to urban alienation from nature?"
        ]
    },
    
    "metadata": {
        "captured_at": datetime.now().isoformat(),
        "interview_mode": "image_analysis",
        "source_images": [
            "Coffee shop interior with patrons and plants",
            "Self-portrait on city street",
            "Coffee shop interior showing counter and yellow tile floor"
        ]
    }
}

if __name__ == "__main__":
    # Save the scene
    repo = MemoirRepo()
    scene_id = repo.save_scene(scene_data)
    
    print(f"\n✓ Coffee shop scene captured from images!")
    print(f"  ID: {scene_id}")
    print(f"  Title: {scene_data['title']}")
    print(f"  Date: {scene_data['date']}")
    print(f"  Location: {scene_data['location']}")
    print(f"\nKey observations:")
    print(f"  - Botanical interior creating intimate pockets")
    print(f"  - Academic/design work in third place")
    print(f"  - Morning ritual of public solitude")
    print(f"  - Books as identity markers and genuine tools")
    print(f"\nTo view all scenes:")
    print(f"  python3 probe/memoir_manager.py --list-scenes")
