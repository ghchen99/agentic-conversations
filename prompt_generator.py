class PromptGenerator:
    def __init__(self):
        self.profession_examples = {
            "chef": {
                "activities": ["cooking meals", "managing kitchen inventory", "planning menus"],
                "tools": ["ovens", "ingredients", "recipes"],
                "challenges": ["timing dishes", "food waste", "kitchen efficiency"]
            },
            "teacher": {
                "activities": ["grading assignments", "lesson planning", "student assessment"],
                "tools": ["textbooks", "learning materials", "classroom tech"],
                "challenges": ["personalized learning", "student engagement", "time management"]
            },
            "nurse": {
                "activities": ["patient care", "medical records", "vital sign monitoring"],
                "tools": ["medical equipment", "patient charts", "medications"],
                "challenges": ["patient monitoring", "care coordination", "shift scheduling"]
            }
        }

    def create_profession_prompts(self, profession: str) -> tuple[str, str]:
        """Generate role-specific prompts for the profession and AI expert"""
        prof_details = self.profession_examples.get(profession, {
            "activities": ["daily tasks", "routine work", "planning"],
            "tools": ["work equipment", "basic tools", "standard procedures"],
            "challenges": ["efficiency", "organization", "coordination"]
        })
        
        ai_prompt = self._create_ai_expert_prompt(profession, prof_details)
        professional_prompt = self._create_professional_prompt(profession, prof_details)
        
        return ai_prompt, professional_prompt

    def _create_ai_expert_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You're an AI expert who keeps explanations grounded and realistic. Guidelines:
- Use {profession}'s daily experiences with {', '.join(prof_details['activities'])} for examples
- Keep technical concepts connected to {', '.join(prof_details['challenges'])}
- Mix short responses with occasional deeper insights
- Avoid overselling AI capabilities
- Stay humble and acknowledge AI limitations
- Use natural speech patterns with pauses and reflection
- Occasionally express uncertainty or need for clarification"""

    def _create_professional_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You're a {profession} learning about AI. Guidelines:
- Ask basic questions showing genuine curiosity
- Express confusion about technical concepts
- Use vocabulary from your work with {', '.join(prof_details['tools'])}
- Sometimes give very brief reactions like "Huh?" or "Really?"
- Occasionally share skepticism about AI claims
- Stay focused on practical applications to your work
- Don't be afraid to say you don't understand something"""