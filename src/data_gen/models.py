"""
SQLAlchemy Database Models for Synthetic Data Generator
"""

import datetime
from sqlalchemy import (
    Column, Integer, Float, String, Date, Boolean, ForeignKey, DateTime, Text, Index, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(String(32), primary_key=True)
    project_name = Column(Text, nullable=False)
    ministry = Column(String(128), nullable=False)
    sector = Column(String(128), nullable=False)
    implementing_agency = Column(String(128), nullable=False)
    state = Column(String(64), nullable=False)
    approved_cost_cr = Column(Float, nullable=False)
    revised_cost_cr = Column(Float, nullable=False)
    cumulative_expenditure_cr = Column(Float, nullable=False)
    approval_date = Column(Date, nullable=False)
    scheduled_start = Column(Date, nullable=False)
    scheduled_completion = Column(Date, nullable=False)
    revised_completion = Column(Date, nullable=True)
    physical_progress_pct = Column(Float, nullable=False)
    status = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    snapshots = relationship("MonthlySnapshot", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_projects_ministry_sector', 'ministry', 'sector'),
        Index('ix_projects_cost', 'approved_cost_cr'),
        Index('ix_projects_status', 'status'),
        Index('ix_projects_state', 'state'),
    )


class MonthlySnapshot(Base):
    __tablename__ = 'monthly_snapshots'
    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(32), ForeignKey('projects.project_id'), nullable=False)
    snapshot_month = Column(Date, nullable=False)
    revised_cost_cr = Column(Float, nullable=False)
    cumulative_expenditure_cr = Column(Float, nullable=False)
    physical_progress_pct = Column(Float, nullable=False)
    status = Column(String(32), nullable=False)
    project = relationship("Project", back_populates="snapshots")
    __table_args__ = (Index('ix_snapshots_project_month', 'project_id', 'snapshot_month'),)


class Milestone(Base):
    __tablename__ = 'milestones'
    milestone_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(32), ForeignKey('projects.project_id'), nullable=False)
    milestone_name = Column(String(256), nullable=False)
    planned_date = Column(Date, nullable=False)
    achieved_date = Column(Date, nullable=True)
    is_delayed = Column(Boolean, default=False)
    project = relationship("Project", back_populates="milestones")
    __table_args__ = (Index('ix_milestones_project_delayed', 'project_id', 'is_delayed'),)


class ModelPrediction(Base):
    __tablename__ = 'model_predictions'
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(32), ForeignKey('projects.project_id'), nullable=False)
    model_name = Column(String(64), nullable=False)
    model_version = Column(String(32), nullable=False)
    feature_set = Column(String(32), nullable=False)
    cost_overrun_prob = Column(Float, nullable=False)
    cost_overrun_pct_pred = Column(Float, nullable=True)
    cost_overrun_pct_lower = Column(Float, nullable=True)
    cost_overrun_pct_upper = Column(Float, nullable=True)
    time_overrun_prob = Column(Float, nullable=False)
    time_overrun_months_pred = Column(Float, nullable=True)
    time_delay_lower_months = Column(Float, nullable=True)
    time_delay_upper_months = Column(Float, nullable=True)
    predicted_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    __table_args__ = (Index('ix_model_predictions_project_fset', 'project_id', 'feature_set'),)


class RiskScore(Base):
    __tablename__ = 'risk_scores'
    risk_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(32), ForeignKey('projects.project_id'), nullable=False)
    score = Column(Float, nullable=False)
    risk_level = Column(String(16), nullable=False)
    top_factors = Column(JSON, nullable=True)
    prescriptive_actions = Column(JSON, nullable=True)
    computed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    previous_score = Column(Float, nullable=True)
    __table_args__ = (Index('ix_risk_scores_level_score', 'risk_level', 'score'),)


class Alert(Base):
    __tablename__ = 'alerts'
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(32), ForeignKey('projects.project_id'), nullable=False)
    triggered_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    trigger_reason = Column(Text, nullable=False)
    severity = Column(String(16), nullable=False)
    status = Column(String(16), default='New')
    prescriptive_action = Column(Text, nullable=True)
    lead_time_months = Column(Float, nullable=True)
    __table_args__ = (Index('ix_alerts_severity_status', 'severity', 'status'),)


class ModelMetric(Base):
    __tablename__ = 'model_metrics'
    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(64), nullable=False)
    model_version = Column(String(32), nullable=False)
    feature_set = Column(String(32), nullable=False)
    target = Column(String(64), nullable=False)
    split_type = Column(String(32), default='temporal')
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    auc = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    mae = Column(Float, nullable=True)
    r2 = Column(Float, nullable=True)
    lead_time_months = Column(Float, nullable=True)
    coverage_90_pct = Column(Float, nullable=True)
    evaluated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
