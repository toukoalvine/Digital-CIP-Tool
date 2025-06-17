# Digital-CIP-Tool
A comprehensive web-based tool for managing continuous improvement projects using the PDCA (Plan-Do-Check-Act) methodology.
# Digital CIP Tool (Continuous Improvement Process)

A comprehensive web-based tool for managing continuous improvement projects using the PDCA (Plan-Do-Check-Act) methodology.

## 🎯 Features

- **PDCA Workflow Management**: Structured approach through Plan, Do, Check, and Act phases
- **Task Tracking**: Assign responsibilities, set deadlines, and track progress
- **Visual Dashboards**: Interactive charts and progress indicators
- **Project Management**: Multiple project support with status tracking
- **Role-based Access**: Admin, Editor, and Reader roles
- **Export Functionality**: Download projects as JSON files
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📋 How to Use

### 1. Creating a Project

- Click "➕ New Project" in the sidebar to create a new CIP project
- Or click "📝 Load Sample Project" to see an example

### 2. PDCA Phases

#### Plan Phase 📋
- Define the problem clearly and measurably
- Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Conduct root cause analysis using methods like 5-Why or Ishikawa diagram
- Plan specific actions to address the problem

#### Do Phase 🔨
- Add and manage implementation tasks
- Assign responsibilities and set due dates
- Track task status (Open, In Progress, Completed)
- Monitor progress in real-time

#### Check Phase 📊
- Enter before and after metrics
- Assess results and calculate improvements
- Document findings and outcomes

#### Act Phase 🎯
- Standardize successful improvements
- Document lessons learned
- Plan next steps and follow-up actions

### 3. Dashboard 📈

View comprehensive project analytics including:
- Task completion metrics
- Status distribution charts
- Improvement comparisons
- Progress indicators

### 4. User Roles

- **Admin**: Full access to all features including project deletion
- **Editor**: Can create and modify projects and tasks
- **Reader**: View-only access to projects

## 💡 Best Practices

1. **Problem Definition**: Be specific and measurable in your problem statements
2. **Root Cause Analysis**: Use structured methods like 5-Why to identify true causes
3. **SMART Goals**: Ensure goals are Specific, Measurable, Achievable, Relevant, and Time-bound
4. **Regular Updates**: Keep task status current for accurate progress tracking
5. **Documentation**: Thoroughly document lessons learned for future reference

## 🔧 Technical Details

### Built With

- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Python**: Core programming language

### Data Storage

- Projects are stored in browser session state
- No external database required
- Export functionality available for data persistence

## 📁 Project Structure

```
digital-cip-tool/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore file (optional)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Report bugs or issues
2. Suggest new features
3. Submit pull requests
4. Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the tool tour within the application
2. Review this README file
3. Create an issue in the project repository

## 🔄 Version History

- **v1.0.0**: Initial release with core PDCA functionality
- Features: Project management, task tracking, dashboard, export functionality

---

**Happy Continuous Improving! 🚀**
