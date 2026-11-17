# pyright: reportMissingImports=false
"""
arcade.dialogues — Context-Aware Dialogue Engine for OILS-3.
Provides 40+ authentic, non-AI-slop 3rd-sem engineering student banter lines
rotated via no-repeat shuffle decks across Hub, Git, DSA, Java, and Viva screens.
"""

import random

try:
    from arcade.core import Color  # type: ignore
except (ImportError, ValueError):
    from .core import Color  # type: ignore

DIALOGUE_POOLS = {
    "general": [
        "Breathe. Nobody in this batch actually understands all 3 labs either. You're fine.",
        "Your code doesn't have to be art today; it just has to compile before the bell rings.",
        "Powered entirely by cold hostel tap water, instant Maggi, and sheer academic defiance.",
        "Remember: even if your logic is flawed, confidence in front of the lab external is 50% of the grade.",
        "If it compiles with 47 warnings, that still counts as compiling. Let's cook.",
        "Somewhere right now, another 3rd-sem engineer is crying over a missing semicolon. You are not alone.",
        "Rule #1 of engineering lab: if it worked once, don't touch anything, don't breathe on it.",
        "We don't need a miracle today, we just need the compiler to look the other way for five minutes.",
    ],
    "git": [
        "Merge conflicts build character... or at least teach you never to edit code directly on GitHub web.",
        "If Git says 'fatal: refusing to merge unrelated histories', just know we've all been there.",
        "Rule of thumb: 'WIP: please work' is a valid commit message only when you're 10 minutes from submission.",
        "Detached HEAD state is scary, but so is opening the VTU results portal. You can handle this.",
        "Remember: git fetch is asking politely; git pull is blindly accepting whatever mess your teammate pushed.",
        "A cherry-pick a day keeps the catastrophic branch merge away.",
        "External: 'Why is your branch 14 commits behind main?' You: 'It is a feature-isolated micro-architecture, sir.'",
        "Pushing straight to main on a Friday afternoon is how legends are born (and repositories are ruined).",
    ],
    "dsa": [
        "Segmentation fault (core dumped): C's affectionate way of telling you that pointer belonged to the OS.",
        "Pointers are easy. It's the four asterisks ****ptr in the lab manual that require spiritual guidance.",
        "Remember: free(ptr) gives memory back to RAM; forgetting free() is just donating RAM to the institution.",
        "If your recursion doesn't have a base case, your terminal will give you the deepest sleep of your life.",
        "Circular queue front == rear? Either you're completely full or completely empty. Story of every semester.",
        "A binary search tree is just a binary tree with higher moral standards.",
        "When the external asks the time complexity, saying 'O(n) on average' with enough conviction buys you 30 seconds.",
        "Don't fear the linked list. It's just a bunch of structs holding hands in the dark.",
    ],
    "java": [
        "Welcome to Java, where AbstractProxyFactoryBeanDelegate is considered a concise, readable variable name.",
        "NullPointerException: reminding developers since 1995 that believing something exists doesn't make it real.",
        "The Garbage Collector will clean up your memory leaks eventually. Don't worry, take a sip of tea.",
        "Java examiners love asking the difference between == and .equals(). Don't fall into the trap.",
        "In Java, everything is an Object. Except your happiness during continuous internal evaluations.",
        "Synchronized blocks: because two threads walking into the same critical section is how CPU fistfights start.",
        "Remember: final, finally, and finalize() were named specifically to confuse sleep-deprived students.",
        "If the JVM won't start, blame the environment variables. Everyone else does.",
    ],
    "viva": [
        "Examiner looking at you over their spectacles? Standard intimidation tactic. Hold your ground.",
        "Pro-tip: If you don't know the answer, explain the closest concept you do know with extreme passion.",
        "The examiner already knows you copied the algorithm. They just want to see if you can explain what you copied.",
        "Eye contact, straight back, clear voice. Even printf looks like advanced AI when explained with swagger.",
        "Take 2 seconds before answering each question. It makes you look thoughtful instead of terrified.",
        "When in doubt, draw a box-and-pointer memory diagram. Viva examiners cannot resist a neat diagram.",
        "There are no wrong answers in viva, only answers that lead to 15-minute supplementary questioning.",
        "You survived 2 internal tests and 10 lab manuals. This external examiner is just an NPC with a clipboard.",
    ]
}

THEME_COLORS = {
    "general": Color.YELLOW,
    "git": Color.YELLOW,
    "dsa": Color.GREEN,
    "java": Color.CYAN,
    "viva": Color.YELLOW,
}

class DialogueDeck:
    """
    Maintains independent shuffled decks for each category so that no line
    repeats until all lines in that category have been displayed, and prevents
    back-to-back duplicate lines across deck reshuffle boundaries.
    """
    def __init__(self):
        self._decks = {}
        self._last_line = {}

    def get_line(self, category: str = "general") -> str:
        cat_key = category.lower() if category else "general"
        if cat_key not in DIALOGUE_POOLS:
            cat_key = "general"

        deck = self._decks.get(cat_key)
        if not deck:
            pool = list(DIALOGUE_POOLS[cat_key])
            random.shuffle(pool)
            # Prevent adjacent duplicate across reshuffle
            if len(pool) > 1 and pool[-1] == self._last_line.get(cat_key):
                pool[0], pool[-1] = pool[-1], pool[0]
            self._decks[cat_key] = pool

        line = self._decks[cat_key].pop()
        self._last_line[cat_key] = line
        return line

_GLOBAL_DECK = DialogueDeck()

def get_dialogue(category: str = "general") -> str:
    """Returns the next non-repeating witty dialogue for the given category."""
    return _GLOBAL_DECK.get_line(category)

def print_dialogue(category: str = "general", prefix: str = "  💬 ", newline_after: bool = True):
    """Prints a styled one-liner dialogue with subject-thematic coloring."""
    line = get_dialogue(category)
    color = THEME_COLORS.get((category or "general").lower(), Color.YELLOW)
    end = "\n" if newline_after else ""
    print(f"{prefix}{color}{line}{Color.RESET}{end}")

