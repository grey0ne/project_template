
from sentry_sdk.integrations.django import DjangoIntegration
from dataorm.settings_helpers import config_get_str

from dataorm.base_settings import *

from application.project_settings import *  # type: ignore used to customize templated settings
