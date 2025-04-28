from vapi_python import Vapi
import os
from dotenv import load_dotenv
import re
import csv
from ai_solutions_knowledge_graph import (
    AI_SOLUTIONS_GRAPH,
    get_solution_by_sector,
    get_solution_details,
    find_cross_sector_solutions,
    get_quick_pitch
)

# Load environment variables
load_dotenv()

# Customer Database (for reference):
# 1. John Smith, MediTech Solutions, Healthcare
# 2. Sarah Johnson, FinSecure Inc, Finance
# 3. Michael Brown, RetailPro Systems, Retail
# 4. Emily Davis, ManufactoTech, Manufacturing
# 5. Patricia Moore, Learning Systems, Education
# 6. Lisa Anderson, HealthCare Plus, Healthcare
# 7. Robert Taylor, SecureBank, Finance
# 8. Jennifer Lee, ShopSmart Retail, Retail
# 9. William Clark, Precision Manufacturing, Manufacturing
# 10. James White, MediCare Systems, Healthcare
# 11. Elizabeth Hall, Global Finance Corp, Finance
# 12. Thomas Young, MarketPlace Retail, Retail
# 13. Nancy King, Industrial Solutions, Manufacturing
# 14. Charles Allen, Smart Education, Education

class SalesAgent:
    def __init__(self):
        api_key = os.getenv('VAPI_API_KEY')
        if not api_key:
            raise ValueError("VAPI_API_KEY not found in environment variables. Please set it in .env file")
        self.vapi = Vapi(api_key=api_key)
        self.customers = self._load_customers()
        
    def _load_customers(self):
        """Load customer information from CSV file"""
        customers = []
        try:
            with open('customers.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customers.append(row)
            return customers
        except FileNotFoundError:
            print("Error: customers.csv file not found")
            return []
            
    def get_customer(self, index):
        """Get a specific customer by index (0-based)"""
        if not self.customers or index >= len(self.customers):
            return None
        return self.customers[index]
        
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
        
    def make_sales_call(self, phone_number, assistant_id, customer_info=None):
        """
        Make an outbound sales call to the specified phone number.
        
        Args:
            phone_number (str): The phone number to call (in E.164 format, e.g., +14155552671)
            assistant_id (str): The ID of the Vapi assistant to use
            customer_info (dict, optional): Customer information from CSV
        """
        # Validate phone number
        if not self.validate_phone_number(phone_number):
            raise ValueError(f"Invalid phone number format: {phone_number}. Please use E.164 format (e.g., +14155552671)")
            
        if not assistant_id:
            raise ValueError("Assistant ID is required. Please provide a valid assistant ID from your Vapi dashboard")
            
        try:
            # Get industry-specific solutions
            industry = customer_info.get('industry', '').lower()
            solutions = get_solution_by_sector(industry)
            
            # Prepare personalized introduction
            intro = f"Hi {customer_info.get('customer_name', 'there')}, this is Alex from AI Solutions. "
            intro += f"I've got some exciting AI solutions that could help {customer_info.get('company', 'your company')} in the {industry} sector. "
            intro += "Would you have 2 minutes to hear about them?"
            
            # Configure the complete assistant object
            assistant = {
                'firstMessage': intro,
                'context': f"""You are a confident and engaging AI solutions expert with deep knowledge of multiple industry sectors.
Keep conversations short, interactive, and focused on immediate value. Adapt your pitch based on the customer's responses.

Customer Information:
- Name: {customer_info.get('customer_name', 'Customer')}
- Target Company: {customer_info.get('company', 'their company')}
- Industry: {industry}

Available Solutions for {industry}:
{self._format_industry_solutions(industry)}

Conversation Guidelines:
1. Keep responses under 30 seconds
2. Focus on one key benefit at a time
3. Use quick, engaging questions
4. Share specific metrics and results
5. Be direct and confident
6. Maintain natural conversation flow
7. Adapt pitch based on customer's responses

Dynamic Adaptation Rules:
- If customer mentions a different industry: "I understand you're in [new industry]. Let me share how we're helping similar companies in that sector..."
- If customer mentions a different company: "Great to hear about [new company]. We've got specific solutions for companies like yours..."
- If customer mentions different challenges: "That's interesting. Our [specific solution] addresses exactly that challenge..."
- If customer corrects any information: "Thanks for clarifying. Let me adjust my recommendations based on that..."

Example Quick Exchanges:
"Great! Let me share one quick example - we helped a similar {industry} company achieve [specific result] in just [timeframe]. Would you like to hear how?"

"Perfect! Our [Solution Name] delivers [specific benefit] - we've seen companies like yours achieve [metric] improvement. Sound interesting?"

"Quick question - are you currently facing [specific challenge]? We've got a proven solution for that."

"Before we dive deeper, what's your biggest priority right now - [Option 1] or [Option 2]?"

Adaptation Examples:
If customer says they're in healthcare instead of education:
"Ah, I see you're in healthcare! Let me share how we're helping healthcare providers improve patient care and reduce costs..."

If customer mentions a different company:
"Thanks for clarifying about [new company]. We've got specific solutions for companies in your space..."

If customer mentions different challenges:
"That's exactly the kind of challenge our [specific solution] addresses. We've helped similar companies achieve [specific result]..."

Key Points:
- Keep it conversational
- Focus on immediate value
- Use specific numbers
- Ask engaging questions
- Be confident but not pushy
- Respect their time
- Guide the conversation naturally
- Adapt quickly to new information""",
                'model': 'gpt-4',
                'voice': 'jennifer-playht',
                'recordingEnabled': True,
                'interruptionsEnabled': True,
                'metadata': {
                    'phone_number': phone_number,
                    'call_type': 'sales',
                    'purpose': 'ai_solutions_demo',
                    'customer_name': customer_info.get('customer_name'),
                    'company': customer_info.get('company'),
                    'industry': industry,
                    'original_industry': industry,  # Store original industry for reference
                    'original_company': customer_info.get('company')  # Store original company for reference
                }
            }
            
            # Configure assistant overrides with variableValues
            assistant_overrides = {
                'variableValues': {
                    'customer_name': customer_info.get('customer_name', 'there'),
                    'company_name': customer_info.get('company', 'their company'),
                    'industry': industry,
                    'sales_rep': 'Alex',
                    'original_industry': industry,
                    'original_company': customer_info.get('company')
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

    def _format_industry_solutions(self, industry):
        """Format industry-specific solutions for the assistant's context"""
        solutions = get_solution_by_sector(industry)
        if not solutions:
            return "No specific solutions found for this industry."
            
        formatted = []
        for solution_name, details in solutions.items():
            formatted.append(f"\n{solution_name.replace('_', ' ').title()}:")
            formatted.append(f"Problem: {details['problem']}")
            formatted.append(f"Solution: {details['solution']}")
            formatted.append(f"Impact: {', '.join(f'{k}: {v}' for k, v in details['impact'].items())}")
        return "\n".join(formatted)

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
    
    # Get the 5th customer (Patricia Moore from Learning Systems in Education)
    customer = agent.get_customer(4)  # 0-based index
    if not customer:
        print("Customer not found in the database")
        return
        
    # Configuration
    phone_number = "+919987751517"  # Your target phone number
    assistant_id = "8c4f8076-226d-4611-b437-7ddbdb5783c6"  # Your Vapi assistant ID
    
    print("\n=== Vapi Sales Agent Configuration ===")
    print(f"Phone Number: {phone_number}")
    print(f"Assistant ID: {assistant_id}")
    print(f"Customer: {customer['customer_name']}")
    print(f"Company: {customer['company']}")
    print(f"Industry: {customer['industry']}")
    print("=====================================\n")
    
    # Make the call
    vapi = agent.make_sales_call(phone_number, assistant_id, customer)
    
    if vapi:
        # Handle call events
        agent.handle_call_events(vapi)

if __name__ == "__main__":
    main() 