from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Environment variables for the database URL
COURSE_DATABASE_URL = os.getenv("COURSE_DATABASE_URL")

ASSESSMENT_DATABASE_URL = os.getenv("ASSESSMENT_DATABASE_URL")

USER_DATABASE_URL = os.getenv("USER_DATABASE_URL")

LEARNER_DATABASE_URL = os.getenv("LEARNER_DATABASE_URL")

# List of tables to ignore (e.g., master tables)
IGNORE_TABLES = [
    'master_learning_outcomes',
    'proficiencies',
    'competencies',
    'domains',
    'regions',
    'references',
    'resources'
]  # Add your master tables here

user_tables = [
    'password_reset_token',
    'track_user_login',
    'user',
    'user_rbac',
    # 'user_rbac',
    # 'user_hierarchy'
]
assessment_tables = [
    "assessment",
    "assessment_module",
    "course_assessment",
    "assessment_schedule",
    "assessment_participant",
    "assessment_result",
    "standalone_assessment",
    "module_results",
    "temp_assessment_response",
    "audit_log",
    "assessment_request",
    "assessment_tag",
    "user_sga",
    "competency_assessment_response",
    "assessment_certification",
    "learner_skill_assessment",
    "master_questionbank",
    "module",
    "question",
    "question_option",
    "question_bank_tag",
    "remedial_action",
    "master_policy",
    "sga",
    "sga_course",
    "sga_grade",
    "sga_extension"
]

course_tables = [
    "course_requests",
    "courses",
    "course_version_control",
    "course_files",
    "lesson_plans",
    "course_assignments",
    "course_learning_outcomes",
    "approvals",
    "course_resources",
    "course_references",
    "course_prerequisite",
    "curriculum",
    "course_curriculum",
    "user_curriculum",
    "course_intended_audience",
    "pre_course_work",
    "assessment_learning_outcomes",
    "user_comment_status",
    "curriculum_domain",
    "ilp",
    "curriculum_version",
    "audit_log",
    "course_load_factor",
    "course_schedule",
    "location",
    "nomination",
    "replacement_tracker",
    "trainer_association"
]


learner_tables = [
    "attendance",
    "feedback",
    "feedback_group",
    "feedback_response",
    "mentor_domain",
    "mentor_mentee",
    "mentor_session",
    "module_feedback",
    "user_scorm_date"
]
@app.route('/clear-db', methods=['POST'])
def clear_db():
    # DATABASE_URL = COURSE_DATABASE_URL
    # tables_to_truncate = course_tables

    DATABASE_URL = LEARNER_DATABASE_URL
    tables_to_truncate = learner_tables
    # SQLAlchemy sync setup for PostgreSQL using psycopg2
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)

    truncated_tables = []

    try:
        with SessionLocal() as session:
            for table_name in tables_to_truncate:
                # Check if the table is in the ignore list
                if table_name not in IGNORE_TABLES:
                    # Truncate the specified table
                    session.execute(text(f'TRUNCATE TABLE "{table_name}" CASCADE'))
                    truncated_tables.append(table_name)
                else:
                    return jsonify({"error": f"Table '{table_name}' is in the ignore list and cannot be truncated."}), 400
            
            # Commit all changes after truncation
            session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"Tables truncated successfully: {truncated_tables}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)