import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import uuid

# Page configuration
st.set_page_config(
    page_title="Digital CIP Tool",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for better design
st.markdown("""
<style>
    .pdca-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .phase-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    
    .plan-card { border-left-color: #FF6B6B; background-color: #FFE5E5; }
    .do-card { border-left-color: #4ECDC4; background-color: #E5F9F6; }
    .check-card { border-left-color: #45B7D1; background-color: #E5F3FF; }
    .act-card { border-left-color: #96CEB4; background-color: #E5F5E5; }
    
    .task-completed { text-decoration: line-through; opacity: 0.6; }
    .priority-high { border-left: 3px solid #FF4444; }
    .priority-medium { border-left: 3px solid #FFA500; }
    .priority-low { border-left: 3px solid #4CAF50; }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'projects' not in st.session_state:
        st.session_state.projects = {}
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'Admin'  # Simplified for demo
    if 'tasks' not in st.session_state:
        st.session_state.tasks = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

# Create sample project
def create_sample_project():
    sample_id = str(uuid.uuid4())
    return {
        'id': sample_id,
        'name': 'Example: Reducing Wait Times',
        'description': 'Reduce production wait times by 30%',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'in_progress',
        'plan': {
            'problem': 'Long wait times between production steps',
            'goal': 'Reduce wait times by 30%',
            'root_cause': 'Unbalanced machine capacities',
            'measures': ['Machine analysis', 'Process optimization', 'Training']
        },
        'do': {
            'implementation_steps': [
                {'task': 'Analyze machine utilization', 'responsible': 'John Smith', 'due_date': '2024-07-15', 'status': 'completed'},
                {'task': 'Identify bottlenecks', 'responsible': 'Anna Johnson', 'due_date': '2024-07-20', 'status': 'in_progress'},
                {'task': 'Implement optimization measures', 'responsible': 'Tom Wilson', 'due_date': '2024-07-30', 'status': 'open'}
            ]
        },
        'check': {
            'metrics': {'wait_time_before': 45, 'wait_time_after': 32, 'improvement_percent': 28.9},
            'results': 'Wait times were reduced by 28.9%'
        },
        'act': {
            'standardization': 'New work instructions created',
            'lessons_learned': 'Regular capacity analysis is essential',
            'next_steps': 'Extension to other production lines'
        }
    }

# Progress calculation
def calculate_progress(project_data):
    phases = ['plan', 'do', 'check', 'act']
    completed_phases = 0
    
    if project_data.get('plan', {}).get('problem'):
        completed_phases += 0.25
    if project_data.get('do', {}).get('implementation_steps'):
        completed_phases += 0.25
    if project_data.get('check', {}).get('results'):
        completed_phases += 0.25
    if project_data.get('act', {}).get('standardization'):
        completed_phases += 0.25
    
    return min(completed_phases * 100, 100)

# PDCA progress display
def show_pdca_progress(current_phase):
    phases = ['Plan', 'Do', 'Check', 'Act']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    cols = st.columns(4)
    for i, (phase, color) in enumerate(zip(phases, colors)):
        with cols[i]:
            if phase.lower() == current_phase:
                st.markdown(f"""
                <div style="background-color: {color}; color: white; padding: 10px; 
                           border-radius: 5px; text-align: center; font-weight: bold;">
                    {phase} ✓
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; color: #666; padding: 10px; 
                           border-radius: 5px; text-align: center;">
                    {phase}
                </div>
                """, unsafe_allow_html=True)

# Main application
def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="pdca-header">🔄 Digital CIP Tool</div>', unsafe_allow_html=True)
    
    # Sidebar for project selection
    with st.sidebar:
        st.header("Project Selection")
        
        # Create new project
        if st.button("➕ New Project"):
            new_project = {
                'id': str(uuid.uuid4()),
                'name': 'New CIP Project',
                'description': '',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'draft',
                'plan': {}, 'do': {}, 'check': {}, 'act': {}
            }
            st.session_state.projects[new_project['id']] = new_project
            st.session_state.current_project = new_project['id']
            st.rerun()
        
        # Add sample project
        if st.button("📝 Load Sample Project"):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()
        
        # Project list
        if st.session_state.projects:
            project_names = {pid: proj['name'] for pid, proj in st.session_state.projects.items()}
            selected_project = st.selectbox(
                "Active Project:",
                options=list(project_names.keys()),
                format_func=lambda x: project_names[x],
                index=0 if st.session_state.current_project is None else 
                      list(project_names.keys()).index(st.session_state.current_project) 
                      if st.session_state.current_project in project_names else 0
            )
            st.session_state.current_project = selected_project
        
        # User role
        st.selectbox("User Role:", ['Admin', 'Editor', 'Reader'], 
                    index=['Admin', 'Editor', 'Reader'].index(st.session_state.user_role),
                    key='user_role')
    
    # Main content
    if not st.session_state.projects:
        st.info("👋 Welcome! Create a new project or load the sample project.")
        
        # Onboarding info
        with st.expander("🎯 Tool Tour: How the CIP Tool Works"):
            st.markdown("""
            **1. PDCA Cycle:** Work systematically through the four phases
            - **Plan:** Define problem and plan actions
            - **Do:** Implement and track actions
            - **Check:** Review and evaluate results
            - **Act:** Standardize and define next steps
            
            **2. Task Tracking:** Manage to-dos with responsibilities and deadlines
            **3. Visualization:** Dashboards and progress tracking
            **4. Teamwork:** Comments and collaboration
            """)
        return
    
    # Display current project
    current_proj = st.session_state.projects[st.session_state.current_project]
    
    # Project header with progress
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.header(current_proj['name'])
        if st.session_state.user_role in ['Admin', 'Editor']:
            new_name = st.text_input("Project Name:", current_proj['name'], key="proj_name")
            if new_name != current_proj['name']:
                current_proj['name'] = new_name
    
    with col2:
        progress = calculate_progress(current_proj)
        st.metric("Progress", f"{progress:.0f}%")
    
    with col3:
        status_options = ['draft', 'in_progress', 'completed', 'on_hold']
        status_labels = {'draft': '📝 Draft', 'in_progress': '🔄 In Progress', 
                        'completed': '✅ Completed', 'on_hold': '⏸️ On Hold'}
        if st.session_state.user_role in ['Admin', 'Editor']:
            new_status = st.selectbox("Status:", status_options, 
                                    index=status_options.index(current_proj.get('status', 'draft')),
                                    format_func=lambda x: status_labels[x])
            current_proj['status'] = new_status
    
    # Tabs for PDCA phases
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Plan", "🔨 Do", "📊 Check", "🎯 Act", "📈 Dashboard"])
    
    with tab1:  # PLAN
        st.markdown('<div class="phase-card plan-card"><h3>📋 Plan - Planning</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('plan')
        
        if st.session_state.user_role in ['Admin', 'Editor']:
            # Problem definition
            st.subheader("🎯 Problem Definition")
            problem = st.text_area("What is the problem?", 
                                 current_proj.get('plan', {}).get('problem', ''),
                                 help="Describe the problem concretely and measurably")
            
            # Goal setting
            st.subheader("🎯 Goal Setting")
            goal = st.text_area("What is the goal?", 
                              current_proj.get('plan', {}).get('goal', ''),
                              help="SMART goals: Specific, Measurable, Achievable, Relevant, Time-bound")
            
            # Root cause analysis
            st.subheader("🔍 Root Cause Analysis")
            root_cause = st.text_area("What are the main causes?", 
                                    current_proj.get('plan', {}).get('root_cause', ''),
                                    help="Use 5-Why, Ishikawa diagram or other analysis methods")
            
            # Action planning
            st.subheader("📝 Action Planning")
            measures_text = st.text_area("Planned actions (one per line):", 
                                       '\n'.join(current_proj.get('plan', {}).get('measures', [])))
            measures = [m.strip() for m in measures_text.split('\n') if m.strip()]
            
            # Auto-save
            if 'plan' not in current_proj:
                current_proj['plan'] = {}
            current_proj['plan'].update({
                'problem': problem,
                'goal': goal,
                'root_cause': root_cause,
                'measures': measures
            })
        else:
            # Display only for readers
            plan_data = current_proj.get('plan', {})
            if plan_data.get('problem'):
                st.write("**Problem:**", plan_data['problem'])
            if plan_data.get('goal'):
                st.write("**Goal:**", plan_data['goal'])
            if plan_data.get('root_cause'):
                st.write("**Root Causes:**", plan_data['root_cause'])
            if plan_data.get('measures'):
                st.write("**Actions:**")
                for measure in plan_data['measures']:
                    st.write(f"• {measure}")
    
    with tab2:  # DO
        st.markdown('<div class="phase-card do-card"><h3>🔨 Do - Implementation</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('do')
        
        # Task management
        st.subheader("📋 Task Tracking")
        
        if st.session_state.user_role in ['Admin', 'Editor']:
            # Add new task
            with st.expander("➕ Add New Task"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_task = st.text_input("Task:")
                with col2:
                    new_responsible = st.text_input("Responsible:")
                with col3:
                    new_date = st.date_input("Due Date:")
                
                if st.button("Add Task") and new_task:
                    if 'do' not in current_proj:
                        current_proj['do'] = {'implementation_steps': []}
                    if 'implementation_steps' not in current_proj['do']:
                        current_proj['do']['implementation_steps'] = []
                    
                    current_proj['do']['implementation_steps'].append({
                        'task': new_task,
                        'responsible': new_responsible,
                        'due_date': new_date.strftime('%Y-%m-%d'),
                        'status': 'open',
                        'priority': 'medium'
                    })
                    st.rerun()
        
        # Display task list
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        if tasks:
            for i, task in enumerate(tasks):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                    
                    with col1:
                        task_class = "task-completed" if task['status'] == 'completed' else ""
                        st.markdown(f'<div class="{task_class}">{task["task"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.write(f"👤 {task['responsible']}")
                    
                    with col3:
                        st.write(f"📅 {task['due_date']}")
                    
                    with col4:
                        if st.session_state.user_role in ['Admin', 'Editor']:
                            new_status = st.selectbox("", ['open', 'in_progress', 'completed'], 
                                                    index=['open', 'in_progress', 'completed'].index(task['status']),
                                                    key=f"status_{i}")
                            task['status'] = new_status
                    
                    with col5:
                        if st.session_state.user_role == 'Admin':
                            if st.button("🗑️", key=f"delete_{i}"):
                                tasks.pop(i)
                                st.rerun()
                    
                    st.divider()
        else:
            st.info("No tasks defined yet.")
    
    with tab3:  # CHECK
        st.markdown('<div class="phase-card check-card"><h3>📊 Check - Verification</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('check')
        
        if st.session_state.user_role in ['Admin', 'Editor']:
            st.subheader("📈 Metrics & Results")
            
            # Enter metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                metric1 = st.number_input("Before Value:", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('wait_time_before', 0.0))
            with col2:
                metric2 = st.number_input("After Value:", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('wait_time_after', 0.0))
            with col3:
                if metric1 > 0:
                    improvement = ((metric1 - metric2) / metric1) * 100
                    st.metric("Improvement", f"{improvement:.1f}%")
            
            # Results assessment
            results = st.text_area("Results Assessment:", 
                                 current_proj.get('check', {}).get('results', ''))
            
            # Save
            if 'check' not in current_proj:
                current_proj['check'] = {}
            current_proj['check'].update({
                'metrics': {
                    'wait_time_before': metric1,
                    'wait_time_after': metric2,
                    'improvement_percent': improvement if metric1 > 0 else 0
                },
                'results': results
            })
        else:
            # Display only
            check_data = current_proj.get('check', {})
            if check_data.get('metrics'):
                metrics = check_data['metrics']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Before", metrics.get('wait_time_before', 0))
                with col2:
                    st.metric("After", metrics.get('wait_time_after', 0))
                with col3:
                    st.metric("Improvement", f"{metrics.get('improvement_percent', 0):.1f}%")
            
            if check_data.get('results'):
                st.write("**Results:**", check_data['results'])
    
    with tab4:  # ACT
        st.markdown('<div class="phase-card act-card"><h3>🎯 Act - Action</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('act')
        
        if st.session_state.user_role in ['Admin', 'Editor']:
            st.subheader("📋 Standardization & Next Steps")
            
            # Standardization
            standardization = st.text_area("Standardization:", 
                                         current_proj.get('act', {}).get('standardization', ''),
                                         help="How will improvements be permanently anchored?")
            
            # Lessons learned
            lessons = st.text_area("Lessons Learned:", 
                                 current_proj.get('act', {}).get('lessons_learned', ''),
                                 help="What did you learn? What would you do differently?")
            
            # Next steps
            next_steps = st.text_area("Next Steps:", 
                                    current_proj.get('act', {}).get('next_steps', ''),
                                    help="What follow-up actions are planned?")
            
            # Save
            if 'act' not in current_proj:
                current_proj['act'] = {}
            current_proj['act'].update({
                'standardization': standardization,
                'lessons_learned': lessons,
                'next_steps': next_steps
            })
        else:
            # Display only
            act_data = current_proj.get('act', {})
            if act_data.get('standardization'):
                st.write("**Standardization:**", act_data['standardization'])
            if act_data.get('lessons_learned'):
                st.write("**Lessons Learned:**", act_data['lessons_learned'])
            if act_data.get('next_steps'):
                st.write("**Next Steps:**", act_data['next_steps'])
    
    with tab5:  # DASHBOARD
        st.header("📈 Project Dashboard")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
        in_progress_tasks = len([t for t in tasks if t['status'] == 'in_progress'])
        overdue_tasks = len([t for t in tasks if t['status'] != 'completed' and 
                           datetime.strptime(t['due_date'], '%Y-%m-%d') < datetime.now()])
        
        with col1:
            st.metric("Total Tasks", total_tasks)
        with col2:
            st.metric("Completed", completed_tasks, f"{completed_tasks}/{total_tasks}")
        with col3:
            st.metric("In Progress", in_progress_tasks)
        with col4:
            st.metric("Overdue", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks > 0 else None)
        
        # Task status chart
        if tasks:
            status_counts = {}
            for task in tasks:
                status = task['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Task Status Distribution",
                color_discrete_map={
                    'completed': '#4CAF50',
                    'in_progress': '#FFA500',
                    'open': '#FF4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline (if metrics available)
        check_data = current_proj.get('check', {}).get('metrics', {})
        if check_data:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Before', 'After'],
                y=[check_data.get('wait_time_before', 0), check_data.get('wait_time_after', 0)],
                marker_color=['#FF6B6B', '#4CAF50']
            ))
            fig.update_layout(title="Improvement Comparison", yaxis_title="Value")
            st.plotly_chart(fig, use_container_width=True)
    
    # Export functions
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Actions")
    
    if st.sidebar.button("📥 Export Project"):
        project_json = json.dumps(current_proj, indent=2, ensure_ascii=False, default=str)
        st.sidebar.download_button(
            label="💾 Download JSON",
            data=project_json,
            file_name=f"cip_project_{current_proj['name'].replace(' ', '_')}.json",
            mime="application/json"
        )
    
    if st.sidebar.button("🗑️ Delete Project") and st.session_state.user_role == 'Admin':
        if len(st.session_state.projects) > 1:
            del st.session_state.projects[st.session_state.current_project]
            st.session_state.current_project = list(st.session_state.projects.keys())[0]
            st.rerun()
        else:
            st.sidebar.error("Cannot delete the last project.")

if __name__ == "__main__":
    main()
