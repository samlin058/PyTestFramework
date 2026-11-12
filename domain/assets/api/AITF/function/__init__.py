from __future__ import annotations

from domain.assets.api.AITF.function.current_user_view import CurrentUserView
from domain.assets.api.AITF.function.document_view_set import DocumentViewSet
from domain.assets.api.AITF.function.environment_view_set import EnvironmentViewSet
from domain.assets.api.AITF.function.execution_plan_view_set import ExecutionPlanViewSet
from domain.assets.api.AITF.function.execution_record_view_set import ExecutionRecordViewSet
from domain.assets.api.AITF.function.jenkins_webhook_view import JenkinsWebhookView
from domain.assets.api.AITF.function.login_view import LoginView
from domain.assets.api.AITF.function.logout_view import LogoutView
from domain.assets.api.AITF.function.project_view_set import ProjectViewSet
from domain.assets.api.AITF.function.schedule_view_set import ScheduleViewSet
from domain.assets.api.AITF.function.test_case_view_set import TestCaseViewSet
from domain.assets.api.AITF.function.test_script_view_set import TestScriptViewSet
from domain.assets.api.AITF.function.user_view_set import UserViewSet

__all__ = [
    "CurrentUserView",
    "DocumentViewSet",
    "EnvironmentViewSet",
    "ExecutionPlanViewSet",
    "ExecutionRecordViewSet",
    "JenkinsWebhookView",
    "LoginView",
    "LogoutView",
    "ProjectViewSet",
    "ScheduleViewSet",
    "TestCaseViewSet",
    "TestScriptViewSet",
    "UserViewSet",
]
