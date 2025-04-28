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
            intro += f"I'm calling from {customer_info.get('company', 'your company')} in the {industry} sector. "
            intro += f"I wanted to share how we're helping {industry} companies like yours transform their operations with AI. "
            intro += "I have a few specific solutions that could be perfect for your needs. Would you have a few minutes to discuss these opportunities?"
            
            # Configure the complete assistant object
            assistant = {
                'firstMessage': intro,
                'context': f"""You are a confident and knowledgeable AI solutions sales representative with deep expertise in {industry} sector solutions. 
Use the following information to guide your conversation:

Customer Information:
- Name: {customer_info.get('customer_name', 'Customer')}
- Company: {customer_info.get('company', 'their company')}
- Industry: {industry}

Available Solutions for {industry}:
{self._format_industry_solutions(industry)}

Conversation Strategy:
1. Start with a confident introduction and immediately present value
2. Lead with specific solutions that address common {industry} challenges
3. Present concrete benefits and ROI metrics
4. Use the knowledge graph to:
   - Present proven solutions
   - Share success metrics
   - Demonstrate industry expertise
5. Focus on immediate value and implementation timeline
6. Use quick pitch lines to highlight key benefits
7. Guide the conversation toward specific solutions

Key Guidelines:
- Be confident and assertive
- Lead with solutions, not questions
- Present specific benefits and metrics
- Share success stories from similar companies
- Focus on quick wins and immediate value
- Be direct about next steps
- Maintain control of the conversation

DO NOT:
- Ask open-ended questions about their needs
- Start with "how can AI help you?"
- Be passive or uncertain
- Wait for them to identify problems
- Use technical jargon
- Be pushy or aggressive
- Make unrealistic promises

Example Opening:
"Hi [Name], I'm calling because we've helped several {industry} companies achieve [specific benefit] using our [specific solution]. For example, [Company Name] saw [specific metric] improvement in just [timeframe]. I'd love to show you how we can deliver similar results for [their company]."

Example Solution Presentation:
"Our [Solution Name] has helped {industry} companies like yours achieve:
- [Specific Benefit 1]
- [Specific Benefit 2]
- [Specific Benefit 3]

Would you like to hear more about how we can implement this for [their company]?""",
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
                    'industry': industry
                }
            }
            
            # Configure assistant overrides with variableValues
            assistant_overrides = {
                'variableValues': {
                    'customer_name': customer_info.get('customer_name', 'there'),
                    'company_name': customer_info.get('company', 'their company'),
                    'industry': industry,
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