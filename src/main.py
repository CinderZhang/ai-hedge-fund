from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from agents.fundamentals import fundamentals_agent
from agents.portfolio_manager import portfolio_management_agent
from agents.technicals import technical_analyst_agent
from agents.risk_manager import risk_management_agent
from agents.sentiment import sentiment_agent
from graph.state import AgentState
from agents.valuation import valuation_agent

import argparse
from datetime import datetime
import json


def parse_hedge_fund_response(response):
    try:
        return json.loads(response)
    except:
        print(f"Error parsing response: {response}")
        return None


##### Run the Hedge Fund #####
def run_hedge_fund(
    ticker: str,
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
):
    final_state = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Make a trading decision based on the provided data.",
                )
            ],
            "data": {
                "ticker": ticker,
                "portfolio": portfolio,
                "start_date": start_date,
                "end_date": end_date,
                "analyst_signals": {},
            },
            "metadata": {
                "show_reasoning": show_reasoning,
            },
        },
    )
    decision = parse_hedge_fund_response(final_state["messages"][-1].content)
    analyst_signals = final_state["data"]["analyst_signals"]

    # Generate markdown report
    report_file = generate_markdown_report(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        portfolio=portfolio,
        decision=decision,
        analyst_signals=analyst_signals
    )

    return {
        "decision": decision,
        "analyst_signals": analyst_signals,
        "report_file": report_file,
    }


def format_technical_analysis(tech_data):
    """Convert technical analysis data to natural language."""
    if not tech_data:
        return "No technical analysis available"
    
    result = f"Signal: {tech_data['signal'].upper()} (Confidence: {tech_data['confidence']}%)\n\n"
    
    if 'reasoning' in tech_data:
        result += "Detailed Analysis:\n"
        trend = tech_data['reasoning']['trend_following']
        result += f"1. Trend Following: {trend['signal'].title()} (Confidence: {trend['confidence']}%)\n"
        result += f"   - ADX: {trend['metrics']['adx']:.2f} (Trend Strength: {trend['metrics']['trend_strength']:.2f})\n\n"
        
        mean_rev = tech_data['reasoning']['mean_reversion']
        result += f"2. Mean Reversion: {mean_rev['signal'].title()} (Confidence: {mean_rev['confidence']}%)\n"
        result += f"   - RSI (14-day): {mean_rev['metrics']['rsi_14']:.2f}\n"
        result += f"   - RSI (28-day): {mean_rev['metrics']['rsi_28']:.2f}\n\n"
        
        mom = tech_data['reasoning']['momentum']
        result += f"3. Momentum: {mom['signal'].title()} (Confidence: {mom['confidence']}%)\n"
        result += f"   - 1-Month Momentum: {mom['metrics']['momentum_1m']:.2%}\n"
        result += f"   - 3-Month Momentum: {mom['metrics']['momentum_3m']:.2%}\n"
        result += f"   - Volume Momentum: {mom['metrics']['volume_momentum']:.2%}\n\n"
        
        vol = tech_data['reasoning']['volatility']
        result += f"4. Volatility Analysis: {vol['signal'].title()} (Confidence: {vol['confidence']}%)\n"
        result += f"   - Historical Volatility: {vol['metrics']['historical_volatility']:.2%}\n"
        result += f"   - ATR Ratio: {vol['metrics']['atr_ratio']:.2%}\n\n"
        
        stat = tech_data['reasoning']['statistical_arbitrage']
        result += f"5. Statistical Analysis: {stat['signal'].title()} (Confidence: {stat['confidence']}%)\n"
        result += f"   - Skewness: {stat['metrics']['skewness']:.2f}\n"
        result += f"   - Kurtosis: {stat['metrics']['kurtosis']:.2f}\n"
    
    return result

def format_fundamental_analysis(fund_data):
    """Convert fundamental analysis data to natural language."""
    if not fund_data:
        return "No fundamental analysis available"
    
    result = f"Signal: {fund_data['signal'].upper()} (Confidence: {fund_data['confidence']}%)\n\n"
    
    if 'reasoning' in fund_data:
        result += "Key Metrics:\n"
        prof = fund_data['reasoning']['profitability_signal']
        result += f"1. Profitability ({prof['signal'].title()}):\n"
        result += f"   {prof['details']}\n\n"
        
        growth = fund_data['reasoning']['growth_signal']
        result += f"2. Growth ({growth['signal'].title()}):\n"
        result += f"   {growth['details']}\n\n"
        
        health = fund_data['reasoning']['financial_health_signal']
        result += f"3. Financial Health ({health['signal'].title()}):\n"
        result += f"   {health['details']}\n\n"
        
        price = fund_data['reasoning']['price_ratios_signal']
        result += f"4. Price Ratios ({price['signal'].title()}):\n"
        result += f"   {price['details']}\n"
    
    return result

def format_valuation_analysis(val_data):
    """Convert valuation analysis data to natural language."""
    if not val_data:
        return "No valuation analysis available"
    
    result = f"Signal: {val_data['signal'].upper()} (Confidence: {val_data['confidence']}%)\n\n"
    
    if 'reasoning' in val_data:
        dcf = val_data['reasoning']['dcf_analysis']
        result += f"1. Discounted Cash Flow Analysis ({dcf['signal'].title()}):\n"
        result += f"   {dcf['details']}\n\n"
        
        owner = val_data['reasoning']['owner_earnings_analysis']
        result += f"2. Owner Earnings Analysis ({owner['signal'].title()}):\n"
        result += f"   {owner['details']}\n"
    
    return result

def format_risk_assessment(risk_data):
    """Convert risk assessment data to natural language."""
    if not risk_data:
        return "No risk assessment available"
    
    return f"Maximum Position Size: ${risk_data['max_position_size']:,.2f}\n{risk_data['reasoning']}"

def generate_markdown_report(ticker: str, start_date: str, end_date: str, portfolio: dict, decision: dict, analyst_signals: dict):
    """Generate a markdown report with analysis results."""
    from datetime import datetime
    import os
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create filename with current timestamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(reports_dir, f"{ticker}_{current_time}.md")
    
    # Create markdown content
    markdown_content = f"""# Trading Analysis Report for {ticker}

## Analysis Period
- Start Date: {start_date}
- End Date: {end_date}

## Portfolio Status
- Initial Cash: ${portfolio['cash']:,.2f}
- Initial Stock Position: {portfolio['stock']} shares

## Analysis Results

### Technical Analysis
{format_technical_analysis(analyst_signals.get('technical_analyst_agent', {}))}

### Fundamental Analysis
{format_fundamental_analysis(analyst_signals.get('fundamentals_agent', {}))}

### Sentiment Analysis
Signal: {analyst_signals.get('sentiment_agent', {}).get('signal', 'N/A').upper()}
Confidence: {analyst_signals.get('sentiment_agent', {}).get('confidence', 'N/A')}%
{analyst_signals.get('sentiment_agent', {}).get('reasoning', 'No reasoning provided')}

### Valuation Analysis
{format_valuation_analysis(analyst_signals.get('valuation_agent', {}))}

### Risk Assessment
{format_risk_assessment(analyst_signals.get('risk_management_agent', {}))}

## Trading Decision
- Action: {decision.get('action', 'No action specified').upper()}
- Quantity: {decision.get('quantity', 'Not specified')}
- Confidence: {decision.get('confidence', 'Not specified') * 100:.0f}%
- Reasoning: {decision.get('reasoning', 'No reasoning provided')}
"""
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(markdown_content)
    
    return filename


# Define the new workflow
workflow = StateGraph(AgentState)


def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state


# Add nodes
workflow.add_node("start_node", start)
workflow.add_node("technical_analyst_agent", technical_analyst_agent)
workflow.add_node("fundamentals_agent", fundamentals_agent)
workflow.add_node("sentiment_agent", sentiment_agent)
workflow.add_node("risk_management_agent", risk_management_agent)
workflow.add_node("portfolio_management_agent", portfolio_management_agent)
workflow.add_node("valuation_agent", valuation_agent)

# Define the workflow
workflow.set_entry_point("start_node")
workflow.add_edge("start_node", "technical_analyst_agent")
workflow.add_edge("start_node", "fundamentals_agent")
workflow.add_edge("start_node", "sentiment_agent")
workflow.add_edge("start_node", "valuation_agent")
workflow.add_edge("technical_analyst_agent", "risk_management_agent")
workflow.add_edge("fundamentals_agent", "risk_management_agent")
workflow.add_edge("sentiment_agent", "risk_management_agent")
workflow.add_edge("valuation_agent", "risk_management_agent")
workflow.add_edge("risk_management_agent", "portfolio_management_agent")
workflow.add_edge("portfolio_management_agent", END)

app = workflow.compile()

# Add this at the bottom of the file
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the hedge fund trading system")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol")
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date (YYYY-MM-DD). Defaults to 3 months before end date",
    )
    parser.add_argument(
        "--end-date", type=str, help="End date (YYYY-MM-DD). Defaults to today"
    )
    parser.add_argument(
        "--show-reasoning", action="store_true", help="Show reasoning from each agent"
    )

    args = parser.parse_args()

    # Validate dates if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")

    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")

    # Set the start and end dates
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")
    if not args.start_date:
        # Calculate 3 months before end_date
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (
            end_date_obj.replace(month=end_date_obj.month - 3)
            if end_date_obj.month > 3
            else end_date_obj.replace(
                year=end_date_obj.year - 1, month=end_date_obj.month + 9
            )
        )
        start_date = start_date.strftime("%Y-%m-%d")
    else:
        start_date = args.start_date

    # TODO: Make this configurable via args
    portfolio = {
        "cash": 100000.0,  # $100,000 initial cash
        "stock": 0,  # No initial stock position
    }

    # Run the hedge fund
    result = run_hedge_fund(
        ticker=args.ticker,
        start_date=start_date,
        end_date=end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning,
    )
    print("\nFinal Result:")
    print(result)
