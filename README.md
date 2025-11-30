# GitHub Analytics with Multi-Agent System

A powerful analytics platform that leverages multiple AI agents to analyze GitHub repository data, generate insights, and visualize metrics through an interactive Streamlit interface.

## Features

- Multi-agent architecture for code generation, execution, and review
- Interactive web interface using Streamlit
- GitHub repository data analysis and visualization
- Code quality assessment and scoring
- Support for various data visualizations (matplotlib, plotly)
- PostgreSQL database integration

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- GitHub Personal Access Token
- OpenAI API Key (for LangChain and AI features)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   GITHUB_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=postgresql://username:password@localhost:5432/github_analytics
   ```

## Database Setup

1. Create a new PostgreSQL database:
   ```sql
   CREATE DATABASE github_analytics;
   ```

2. The required tables will be created automatically when you run the data collection notebook.

## Data Collection

1. **Run the Jupyter notebook** to collect GitHub repository data:
   ```bash
   jupyter notebook src/get_github_repos.ipynb
   ```
   - Follow the instructions in the notebook to collect data from GitHub repositories.
   - The notebook will store the data in your PostgreSQL database.

## Running the Application

1. **Start the Streamlit application**:
   ```bash
   cd src
   streamlit run main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

3. Enter your analytics question in the text area and click "Run" to see the results.

## Project Structure

- `src/` - Main source code
  - `main.py` - Streamlit web interface
  - `orchestrator.py` - Coordinates the multi-agent system
  - `writer_agent.py` - Generates code for data analysis
  - `reviewer_agent.py` - Reviews and scores the generated code
  - `executor_agent.py` - Executes the generated code safely
  - `get_github_repos.ipynb` - Jupyter notebook for data collection
  - `requirements.txt` - Python dependencies

## Usage Examples

1. **Basic Analytics**
   - "Show the most active repositories by number of commits"
   - "Plot the trend of issues over time"
   - "Compare pull request statistics between repositories"

2. **Advanced Queries**
   - "Predict the number of issues for the next month"
   - "Analyze the sentiment of issue comments"
   - "Visualize the relationship between stars and forks"

## Troubleshooting

- **Database Connection Issues**: Ensure PostgreSQL is running and the connection string in `.env` is correct.
- **GitHub API Rate Limits**: If you hit rate limits, wait before making more requests or use a GitHub token with higher limits.
- **Missing Dependencies**: Make sure all dependencies are installed from `requirements.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, please open an issue in the repository or contact the maintainers.
