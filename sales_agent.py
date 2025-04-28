from vapi_python import Vapi
import os
from dotenv import load_dotenv
import re
from ai_solutions_knowledge_graph import (
    AI_SOLUTIONS_GRAPH,
    get_solution_by_sector,
    get_solution_details,
    find_cross_sector_solutions,
    get_quick_pitch
)

# Load environment variables
load_dotenv()

class SalesAgent:
    def __init__(self):
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            raise ValueError("VAPI_API_KEY not found in environment variables. Please set it in .env file")
        self.vapi = Vapi(api_key=api_key)
        
    def validate_phone_number(self, phone_number):
        """
        Validate phone number format (E.164)
        
        Args:
            phone_number (str): The phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone_number))
        
    def make_sales_call(self, phone_number, assistant_id, customer_name=None):
        """
        Make an outbound sales call to the specified phone number.
        
        Args:
            phone_number (str): The phone number to call (in E.164 format, e.g., +14155552671)
            assistant_id (str): The ID of the Vapi assistant to use
            customer_name (str, optional): The name of the customer for personalization
        """
        # Validate phone number
        if not self.validate_phone_number(phone_number):
            raise ValueError(f"Invalid phone number format: {phone_number}. Please use E.164 format (e.g., +14155552671)")
            
        if not assistant_id:
            raise ValueError("Assistant ID is required. Please provide a valid assistant ID from your Vapi dashboard")
            
        try:
            # Configure the complete assistant object
            assistant = {
                'firstMessage': f"Hi {customer_name if customer_name else 'there'}, this is Alex from AI Solutions. I hope you're doing well today. I'd love to learn more about your business and explore how AI could help streamline your operations. Would you have a few minutes to chat?",
                'context': f"""You are an experienced AI solutions sales representative with deep knowledge of AI applications across industries. Use the following knowledge graph to guide your conversation and solution recommendations:

Available Sectors and Solutions:
{self._format_solutions_overview()}

Conversation Strategy:
1. Start with a warm greeting and build rapport
2. Ask about their industry and specific challenges
3. Listen for keywords that match knowledge graph nodes
4. Use the graph to:
   - Identify relevant solutions
   - Draw parallels from other industries
   - Present specific impact metrics
   - Offer cross-sector insights
5. Focus on business outcomes, not technical details
6. Use quick pitch lines naturally in conversation
7. Connect their pain points to specific solutions in the graph

Key Guidelines:
- Be conversational and natural
- Listen more than you speak
- Ask open-ended questions
- Take notes of their specific needs
- Present solutions that directly address their pain points
- Be enthusiastic but not pushy
- Focus on value and outcomes

DO NOT:
- Jump straight into product features
- Use technical jargon
- Be pushy or aggressive
- Make unrealistic promises
- Rush the conversation
- Ignore their specific needs""",
                'model': 'gpt-4',
                'voice': 'jennifer-playht',
                'recordingEnabled': True,
                'interruptionsEnabled': True,
                'metadata': {
                    'phone_number': phone_number,
                    'call_type': 'sales',
                    'purpose': 'ai_solutions_demo',
                    'customer_name': customer_name
                }
            }
            
            # Configure assistant overrides with variableValues
            assistant_overrides = {
                'variableValues': {
                    'customer_name': customer_name if customer_name else 'there',
                    'company_name': 'AI Solutions Inc',
                    'sales_rep': 'Alex'
                }
            }
            
            # Start the call with both assistant and overrides
            self.vapi.start(
                assistant=assistant,
                assistant_overrides=assistant_overrides
            )
            
            print("Call started successfully")
            return self.vapi
            
        except Exception as e:
            print(f"Error making sales call: {str(e)}")
            return None

    def _format_solutions_overview(self):
        """Format the solutions overview for the assistant's context."""
        overview = []
        for sector, solutions in AI_SOLUTIONS_GRAPH.items():
            overview.append(f"\n{sector.upper()} SECTOR:")
            for solution_name, details in solutions.items():
                overview.append(f"- {solution_name.replace('_', ' ').title()}")
                overview.append(f"  Problem: {details['problem']}")
                overview.append(f"  Solution: {details['solution']}")
                overview.append(f"  Impact: {', '.join(f'{k}: {v}' for k, v in details['impact'].items())}")
                overview.append(f"  Cross-sector: Similar to {details['cross_sector']['similar_to'].replace('_', ' ').title()}")
        return "\n".join(overview)

    def handle_call_events(self, vapi):
        """
        Handle events from an ongoing call.
        
        Args:
            vapi: The Vapi instance
        """
        try:
            while True:
                # The SDK handles events internally
                # We can add custom event handling here if needed
                pass
        except KeyboardInterrupt:
            print("\nEnding call...")
            vapi.stop()

def main():
    # Initialize the sales agent
    agent = SalesAgent()
    
    # Configuration
    phone_number = "+919987751517"  # Your target phone number
    assistant_id = "8c4f8076-226d-4611-b437-7ddbdb5783c6"  # Your Vapi assistant ID
    customer_name = "John"  # Optional: Customer name for personalization
    
    print("\n=== Vapi Sales Agent Configuration ===")
    print(f"Phone Number: {phone_number}")
    print(f"Assistant ID: {assistant_id}")
    print(f"Customer Name: {customer_name}")
    print("=====================================\n")
    
    # Make the call
    vapi = agent.make_sales_call(phone_number, assistant_id, customer_name)
    
    if vapi:
        # Handle call events
        agent.handle_call_events(vapi)

if __name__ == "__main__":
    main() 