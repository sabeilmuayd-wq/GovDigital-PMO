import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, timedelta
import plotly.express as px
import folium
from streamlit_folium import folium_static

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="GovDigital PMO - إدارة المشاريع الرقمية",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PWA Support ====================
st.markdown("""
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#e74c3c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="GovDigital PMO">
<link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/1674/1674083.png">
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(function(registration) {
      console.log('Service Worker registered');
    })
    .catch(function(error) {
      console.log('Service Worker registration failed:', error);
    });
}
</script>
<style>
    .main-header {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .project-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid #e74c3c;
    }
    .status-green { border-left-color: #2ecc71; }
    .status-yellow { border-left-color: #f39c12; }
    .status-red { border-left-color: #e74c3c; }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== إعداد اللغة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

translations = {
    "en": {
        "title": "🏛️ GovDigital PMO",
        "subtitle": "Government Digital Project Management Office",
        "warning": "⚠️ 70% of government digital projects fail. This system ensures your projects succeed.",
        "projects": "📋 Projects",
        "new_project": "➕ New Project",
        "reports": "📊 Reports",
        "wiki": "📚 Knowledge Base",
        "vendors": "👥 Vendor Ratings",
        "dashboard": "📈 Dashboard",
        "project_name": "Project Name",
        "ministry": "Ministry",
        "budget": "Budget (UGX)",
        "deadline": "Deadline",
        "manager": "Project Manager",
        "description": "Description",
        "add_project": "➕ Add Project",
        "total_projects": "Total Projects",
        "total_budget": "Total Budget",
        "delayed_projects": "Delayed Projects",
        "at_risk": "At Risk",
        "on_track": "On Track",
        "completed": "Completed",
        "delayed": "Delayed",
        "status": "Status",
        "progress": "Progress",
        "phases": "Project Phases",
        "initiation": "Initiation",
        "planning": "Planning",
        "execution": "Execution",
        "monitoring": "Monitoring",
        "closure": "Closure",
        "add_task": "Add Task",
        "task_name": "Task Name",
        "assigned_to": "Assigned To",
        "due_date": "Due Date",
        "save": "Save",
        "no_projects": "No projects yet",
        "export_csv": "📥 Export CSV",
        "knowledge_base": "📚 Knowledge Base",
        "lessons_learned": "Lessons Learned",
        "best_practices": "Best Practices",
        "vendor_name": "Vendor Name",
        "rating": "Rating",
        "previous_projects": "Previous Projects",
        "add_vendor": "Add Vendor",
        "admin_password": "Admin Password",
        "login": "Login",
        "logout": "Logout",
        "pilot_mode": "Pilot Mode"
    },
    "ar": {
        "title": "🏛️ GovDigital PMO",
        "subtitle": "مكتب إدارة المشاريع الرقمية الحكومية",
        "warning": "⚠️ 70% من المشاريع الرقمية الحكومية تفشل. هذا النظام يضمن نجاح مشاريعك.",
        "projects": "📋 المشاريع",
        "new_project": "➕ مشروع جديد",
        "reports": "📊 التقارير",
        "wiki": "📚 قاعدة المعرفة",
        "vendors": "👥 تقييم المطورين",
        "dashboard": "📈 لوحة التحكم",
        "project_name": "اسم المشروع",
        "ministry": "الوزارة",
        "budget": "الميزانية (شلن)",
        "deadline": "تاريخ التسليم",
        "manager": "المدير المسؤول",
        "description": "الوصف",
        "add_project": "➕ إضافة مشروع",
        "total_projects": "إجمالي المشاريع",
        "total_budget": "إجمالي الميزانية",
        "delayed_projects": "مشاريع متأخرة",
        "at_risk": "معرض للخطر",
        "on_track": "في المسار",
        "completed": "مكتمل",
        "delayed": "متأخر",
        "status": "الحالة",
        "progress": "التقدم",
        "phases": "مراحل المشروع",
        "initiation": "البدء",
        "planning": "التخطيط",
        "execution": "التنفيذ",
        "monitoring": "المراقبة",
        "closure": "الإغلاق",
        "add_task": "إضافة مهمة",
        "task_name": "اسم المهمة",
        "assigned_to": "مسند إلى",
        "due_date": "تاريخ الاستحقاق",
        "save": "حفظ",
        "no_projects": "لا توجد مشاريع بعد",
        "export_csv": "📥 تصدير CSV",
        "knowledge_base": "📚 قاعدة المعرفة",
        "lessons_learned": "الدروس المستفادة",
        "best_practices": "أفضل الممارسات",
        "vendor_name": "اسم المطور",
        "rating": "التقييم",
        "previous_projects": "مشاريع سابقة",
        "add_vendor": "إضافة مطور",
        "admin_password": "كلمة المرور",
        "login": "دخول",
        "logout": "خروج",
        "pilot_mode": "وضع التجربة"
    }
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# ==================== إعدادات ====================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "pilot_mode" not in st.session_state:
    st.session_state.pilot_mode = False

# ==================== ملفات البيانات ====================
DATA_FOLDER = "govdigital_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PROJECTS_FILE = os.path.join(DATA_FOLDER, "projects.json")
TASKS_FILE = os.path.join(DATA_FOLDER, "tasks.json")
VENDORS_FILE = os.path.join(DATA_FOLDER, "vendors.json")
KNOWLEDGE_FILE = os.path.join(DATA_FOLDER, "knowledge.json")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== دوال المشاريع ====================
def get_project_status(progress, deadline):
    today = datetime.now().date()
    deadline_date = datetime.fromisoformat(deadline).date()
    
    if progress >= 100:
        return "completed", "🟢", "مكتمل"
    elif deadline_date < today:
        return "delayed", "🔴", "متأخر"
    elif progress < 30:
        return "at_risk", "🟠", "معرض للخطر"
    else:
        return "on_track", "🟡", "في المسار"

def generate_report():
    projects = load_data(PROJECTS_FILE)
    tasks = load_data(TASKS_FILE)
    
    report = {
        "date": datetime.now().isoformat(),
        "total_projects": len(projects),
        "total_budget": sum([p.get("budget", 0) for p in projects]),
        "completed": len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "completed"]),
        "delayed": len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "delayed"]),
        "at_risk": len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "at_risk"]),
        "total_tasks": len(tasks),
        "completed_tasks": len([t for t in tasks if t.get("status") == "completed"])
    }
    return report

# ==================== العنوان ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='warning-box'>
    {t('warning')}
</div>
""", unsafe_allow_html=True)

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"### 🌍 {t('language')}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 English", key="lang_en", use_container_width=True):
            st.session_state.language = "en"
            st.rerun()
    with col2:
        if st.button("🇸🇦 العربية", key="lang_ar", use_container_width=True):
            st.session_state.language = "ar"
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"### 📊 {t('dashboard')}")
    
    report = generate_report()
    st.metric(t("total_projects"), report["total_projects"])
    st.metric(t("total_budget"), f"{report['total_budget']:,.0f} UGX")
    st.metric(t("delayed_projects"), report["delayed"], delta=f"-{report['delayed']}" if report["delayed"] > 0 else "0")
    
    st.markdown("---")
    st.markdown(f"### 🔧 {t('admin_panel')}")
    
    if not st.session_state.admin_logged_in:
        password = st.text_input(t("admin_password"), type="password")
        if st.button(t("login"), use_container_width=True):
            if password == "admin123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Wrong password")
    else:
        if st.button(t("logout"), use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        pilot = st.checkbox(t("pilot_mode"), value=st.session_state.pilot_mode)
        if pilot != st.session_state.pilot_mode:
            st.session_state.pilot_mode = pilot
            st.rerun()
        
        if st.session_state.pilot_mode:
            st.success("✅ Pilot Mode Active")

# ==================== تبويبات التطبيق ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t("projects"), 
    t("new_project"), 
    t("reports"),
    t("wiki"),
    t("vendors")
])

# ==================== TAB 1: المشاريع ====================
with tab1:
    st.subheader(t("projects"))
    
    projects = load_data(PROJECTS_FILE)
    tasks = load_data(TASKS_FILE)
    
    if projects:
        for p in projects:
            status_code, status_icon, status_text = get_project_status(p.get("progress", 0), p.get("deadline", ""))
            status_class = f"status-{status_code}"
            
            with st.expander(f"{status_icon} {p['name']} - {p.get('ministry', 'N/A')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{t('budget')}:** {p.get('budget', 0):,.0f} UGX")
                    st.markdown(f"**{t('deadline')}:** {p.get('deadline', 'N/A')[:10]}")
                    st.markdown(f"**{t('manager')}:** {p.get('manager', 'N/A')}")
                with col2:
                    st.markdown(f"**{t('status')}:** {status_icon} {status_text}")
                    st.markdown(f"**{t('progress')}:** {p.get('progress', 0)}%")
                    st.progress(p.get('progress', 0) / 100)
                
                st.markdown(f"**{t('description')}:** {p.get('description', 'N/A')}")
                
                # عرض المهام المرتبطة
                project_tasks = [t for t in tasks if t.get("project_id") == p["id"]]
                if project_tasks:
                    st.markdown("#### 📋 Tasks")
                    for task in project_tasks:
                        task_status = "✅" if task.get("status") == "completed" else "⏳"
                        st.markdown(f"- {task_status} {task['name']} - {task.get('assigned_to', 'N/A')} (Due: {task.get('due_date', 'N/A')[:10]})")
                
                # إضافة مهمة جديدة
                if st.session_state.admin_logged_in:
                    with st.form(key=f"task_{p['id']}"):
                        st.markdown("#### ➕ Add Task")
                        col1, col2 = st.columns(2)
                        with col1:
                            task_name = st.text_input(t("task_name"), key=f"task_name_{p['id']}")
                            assigned_to = st.text_input(t("assigned_to"), key=f"assigned_{p['id']}")
                        with col2:
                            due_date = st.date_input(t("due_date"), datetime.now(), key=f"due_{p['id']}")
                        if st.form_submit_button(t("add_task")):
                            if task_name:
                                new_task = {
                                    "id": str(uuid.uuid4())[:8],
                                    "project_id": p["id"],
                                    "name": task_name,
                                    "assigned_to": assigned_to,
                                    "due_date": due_date.isoformat(),
                                    "status": "pending",
                                    "created": datetime.now().isoformat()
                                }
                                tasks.append(new_task)
                                save_data(TASKS_FILE, tasks)
                                st.success(f"✅ Task added: {task_name}")
                                st.rerun()
                
                # تحديث التقدم
                if st.session_state.admin_logged_in:
                    new_progress = st.slider(t("progress"), 0, 100, p.get("progress", 0), key=f"progress_{p['id']}")
                    if new_progress != p.get("progress", 0):
                        for proj in projects:
                            if proj["id"] == p["id"]:
                                proj["progress"] = new_progress
                        save_data(PROJECTS_FILE, projects)
                        st.rerun()
    else:
        st.info(t("no_projects"))

# ==================== TAB 2: مشروع جديد ====================
with tab2:
    st.subheader(t("new_project"))
    
    with st.form(key="new_project_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(t("project_name"))
            ministry = st.selectbox(t("ministry"), ["وزارة العلوم والتكنولوجيا", "وزارة الصحة", "وزارة التعليم", "وزارة الزراعة", "NITA-U", "أخرى"])
            budget = st.number_input(t("budget"), min_value=0, step=1_000_000, value=100_000_000)
        with col2:
            deadline = st.date_input(t("deadline"), datetime.now() + timedelta(days=90))
            manager = st.text_input(t("manager"))
        
        description = st.text_area(t("description"), height=100)
        
        # مراحل المشروع (PMO Framework)
        st.markdown(f"### 📋 {t('phases')}")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            initiation = st.checkbox(t("initiation"), value=True)
        with col2:
            planning = st.checkbox(t("planning"))
        with col3:
            execution = st.checkbox(t("execution"))
        with col4:
            monitoring = st.checkbox(t("monitoring"))
        with col5:
            closure = st.checkbox(t("closure"))
        
        submitted = st.form_submit_button(t("add_project"), type="primary", use_container_width=True)
        
        if submitted and name:
            project = {
                "id": str(uuid.uuid4())[:8],
                "name": name,
                "ministry": ministry,
                "budget": budget,
                "deadline": deadline.isoformat(),
                "manager": manager,
                "description": description,
                "progress": 0,
                "phases": {
                    "initiation": initiation,
                    "planning": planning,
                    "execution": execution,
                    "monitoring": monitoring,
                    "closure": closure
                },
                "created": datetime.now().isoformat(),
                "status": "active"
            }
            projects = load_data(PROJECTS_FILE)
            projects.append(project)
            save_data(PROJECTS_FILE, projects)
            st.success(f"✅ {t('add_project')}: {name}")
            st.balloons()
        elif submitted:
            st.error("❌ Please enter project name")

# ==================== TAB 3: التقارير ====================
with tab3:
    st.subheader(t("reports"))
    
    projects = load_data(PROJECTS_FILE)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("total_projects"), len(projects))
    with col2:
        total_budget = sum([p.get("budget", 0) for p in projects])
        st.metric(t("total_budget"), f"{total_budget:,.0f} UGX")
    with col3:
        delayed = len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "delayed"])
        st.metric(t("delayed_projects"), delayed)
    with col4:
        completed = len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "completed"])
        st.metric(t("completed"), completed)
    
    st.markdown("---")
    st.markdown("### 📊 Project Status Distribution")
    
    if projects:
        status_counts = {
            t("on_track"): len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "on_track"]),
            t("at_risk"): len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "at_risk"]),
            t("delayed"): len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "delayed"]),
            t("completed"): len([p for p in projects if get_project_status(p.get("progress", 0), p.get("deadline", ""))[0] == "completed"])
        }
        
        fig = px.pie(values=list(status_counts.values()), names=list(status_counts.keys()), title="Project Status")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Project List")
    
    if projects:
        df = pd.DataFrame(projects)
        display_cols = ["name", "ministry", "budget", "deadline", "manager", "progress"]
        st.dataframe(df[display_cols], use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(t("export_csv"), csv, "govdigital_report.csv", "text/csv")

# ==================== TAB 4: قاعدة المعرفة ====================
with tab4:
    st.subheader(t("wiki"))
    
    knowledge = load_data(KNOWLEDGE_FILE)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 📖 {t('lessons_learned')}")
        lessons = [k for k in knowledge if k.get("type") == "lesson"]
        if lessons:
            for l in lessons[-5:]:
                st.markdown(f"- **{l['title']}** ({l['date'][:10]})<br>{l['content'][:100]}...", unsafe_allow_html=True)
        else:
            st.info("No lessons recorded yet")
    
    with col2:
        st.markdown(f"### 💡 {t('best_practices')}")
        practices = [k for k in knowledge if k.get("type") == "practice"]
        if practices:
            for p in practices[-5:]:
                st.markdown(f"- **{p['title']}**<br>{p['content'][:100]}...", unsafe_allow_html=True)
        else:
            st.info("No best practices recorded yet")
    
    if st.session_state.admin_logged_in:
        st.markdown("---")
        st.markdown("### ➕ Add to Knowledge Base")
        
        with st.form("add_knowledge"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            k_type = st.selectbox("Type", ["lesson", "practice"])
            if st.form_submit_button("Add"):
                if title and content:
                    knowledge.append({
                        "id": str(uuid.uuid4())[:8],
                        "title": title,
                        "content": content,
                        "type": k_type,
                        "date": datetime.now().isoformat()
                    })
                    save_data(KNOWLEDGE_FILE, knowledge)
                    st.success("✅ Added to knowledge base")
                    st.rerun()

# ==================== TAB 5: تقييم المطورين ====================
with tab5:
    st.subheader(t("vendors"))
    
    vendors = load_data(VENDORS_FILE)
    
    if vendors:
        for v in vendors:
            avg_rating = sum(v.get("ratings", [])) / len(v.get("ratings", [])) if v.get("ratings") else 0
            st.markdown(f"""
            <div class='project-card'>
                <strong>{v['name']}</strong><br>
                ⭐ {avg_rating:.1f}/5 ({len(v.get('ratings', []))} reviews)<br>
                📦 {len(v.get('projects', []))} projects completed
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No vendors registered yet")
    
    if st.session_state.admin_logged_in:
        st.markdown("---")
        st.markdown(f"### ➕ {t('add_vendor')}")
        
        with st.form("add_vendor"):
            vendor_name = st.text_input(t("vendor_name"))
            if st.form_submit_button(t("add_vendor")):
                if vendor_name:
                    vendors.append({
                        "id": str(uuid.uuid4())[:8],
                        "name": vendor_name,
                        "ratings": [],
                        "projects": [],
                        "created": datetime.now().isoformat()
                    })
                    save_data(VENDORS_FILE, vendors)
                    st.success(f"✅ Vendor {vendor_name} added")
                    st.rerun()
