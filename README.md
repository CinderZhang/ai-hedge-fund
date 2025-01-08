# AI Hedge Fund

This is a proof concept for an AI-powered hedge fund. The goal of this project is to explore the use of AI to make trading decisions. This project is for **educational** purposes only and is not intended for real trading or investment.

## System Overview

This system employs several specialized agents working together to analyze stocks and make trading decisions:

1. **Valuation Agent**
   - Calculates intrinsic value using DCF analysis
   - Performs owner earnings analysis
   - Generates trading signals based on valuation gaps
   
2. **Sentiment Agent**
   - Analyzes market sentiment indicators
   - Tracks bullish vs bearish signals
   - Provides confidence-weighted sentiment scores

3. **Fundamentals Agent**
   - Analyzes key financial metrics:
     - Profitability (ROE, Net Margin, Operating Margin)
     - Growth (Revenue, Earnings)
     - Financial Health (Current Ratio, D/E)
     - Price Ratios (P/E, P/B, P/S)

4. **Technical Analyst**
   - Performs multi-strategy technical analysis:
     - Trend Following (ADX, Trend Strength)
     - Mean Reversion (RSI, Bollinger Bands)
     - Momentum (1M, 3M, Volume)
     - Volatility Analysis
     - Statistical Arbitrage

5. **Risk Manager**
   - Calculates position size limits
   - Monitors daily trading volume
   - Ensures portfolio risk constraints

6. **Portfolio Manager**
   - Aggregates signals from all agents
   - Makes final trading decisions
   - Generates detailed analysis reports
   
<img width="1060" alt="Screenshot 2025-01-03 at 5 39 25 PM" src="https://github.com/user-attachments/assets/4611aace-27d0-43b2-9a70-385b40336e3f" />

## Features

- **Multi-Agent Architecture**: Each agent specializes in a specific type of analysis
- **Comprehensive Analysis**: Combines technical, fundamental, sentiment, and valuation metrics
- **Risk Management**: Built-in position sizing and risk controls
- **Detailed Reporting**: Generates markdown reports for each analysis with:
  - Analysis period details
  - Portfolio status
  - Technical analysis results
  - Fundamental metrics
  - Sentiment indicators
  - Valuation calculations
  - Risk assessment
  - Trading decisions with confidence levels
- **Backtesting**: Ability to test strategies over historical periods

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No warranties or guarantees provided
- Past performance does not indicate future results
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
  - [Analysis Reports](#analysis-reports)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Setup

Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env

# Required API Keys:
export OPENAI_API_KEY='your-api-key-here'           # Get from https://platform.openai.com/
export FINANCIAL_DATASETS_API_KEY='your-api-key-here' # Get from https://financialdatasets.ai/
```

## Usage

### Running the Hedge Fund

Basic usage:
```bash
poetry run python src/main.py --ticker AAPL
```

Show detailed agent reasoning:
```bash
poetry run python src/main.py --ticker AAPL --show-reasoning
```

Analyze specific time period:
```bash
poetry run python src/main.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-03-01 
```

### Analysis Reports

The system generates detailed markdown reports for each analysis run in the `reports/` directory. Each report is named using the format `{TICKER}_{TIMESTAMP}.md` (e.g., `TSLA_20250108_145300.md`) and includes:

1. **Analysis Period**
   - Start and end dates
   - Portfolio status

2. **Technical Analysis**
   - Overall signal and confidence
   - Detailed metrics for each strategy
   - Performance indicators

3. **Fundamental Analysis**
   - Profitability metrics
   - Growth indicators
   - Financial health measures
   - Valuation ratios

4. **Sentiment Analysis**
   - Market sentiment signal
   - Bullish vs bearish indicators
   - Confidence level

5. **Valuation Analysis**
   - DCF analysis results
   - Owner earnings calculations
   - Market cap comparison
   - Valuation gaps

6. **Risk Assessment**
   - Maximum position size
   - Volume analysis
   - Portfolio constraints

7. **Trading Decision**
   - Recommended action
   - Position size
   - Confidence level
   - Detailed reasoning

### Running the Backtester

Basic backtest:
```bash
poetry run python src/backtester.py --ticker AAPL
```

Backtest specific period:
```bash
poetry run python src/backtester.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-03-01
```

**Example Output:**
```
Starting backtest...
Date         Ticker Action Quantity    Price         Cash    Stock  Total Value
----------------------------------------------------------------------
2024-01-01   AAPL   buy       519.0   192.53        76.93    519.0    100000.00
2024-01-02   AAPL   hold          0   185.64        76.93    519.0     96424.09
2024-01-03   AAPL   hold          0   184.25        76.93    519.0     95702.68
2024-01-04   AAPL   hold          0   181.91        76.93    519.0     94488.22
2024-01-05   AAPL   hold          0   181.18        76.93    519.0     94109.35
2024-01-08   AAPL   sell        519   185.56     96382.57      0.0     96382.57
2024-01-09   AAPL   buy       520.0   185.14       109.77    520.0     96382.57
```

## Project Structure 
```
ai-hedge-fund/
├── reports/                    # Generated analysis reports
├── src/
│   ├── agents/                # Agent definitions and workflow
│   │   ├── fundamentals.py    # Fundamental analysis agent
│   │   ├── portfolio_manager.py # Portfolio management agent
│   │   ├── risk_manager.py    # Risk management agent
│   │   ├── sentiment.py       # Sentiment analysis agent
│   │   ├── technicals.py      # Technical analysis agent
│   │   ├── valuation.py       # Valuation analysis agent
│   ├── tools/                 # Agent tools
│   │   ├── api.py            # API tools and data fetching
│   ├── backtester.py         # Backtesting implementation
│   ├── main.py               # Main entry point
├── pyproject.toml            # Poetry dependency management
├── .env                      # Environment variables
├── README.md                 # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
