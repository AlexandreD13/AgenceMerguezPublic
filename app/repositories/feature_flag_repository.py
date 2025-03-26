from functools import cache
from typing import Optional

from app import models
from app.domain.repositories.feature_flag_repository import IFeatureFlagRepository


class FeatureFlagRepository(IFeatureFlagRepository):

    @cache
    def is_active(self, flag: str, user_email: Optional[str] = None) -> bool:
        global_flag_value = self.__get_global_flag(flag)
        user_flag_value = self.__get_user_flag(flag, user_email)

        if user_flag_value is not None:
            return user_flag_value

        return global_flag_value or False

    def __get_global_flag(self, name: str) -> Optional[bool]:
        return models.FeatureFlag.objects.filter(
            name=name
        ).filter(
            user=None
        ).values_list(
            'value'
        ).first()

    def __get_user_flag(self, name: str, user: str) -> Optional[bool]:
        return models.FeatureFlag.objects.filter(
            name=name
        ).filter(
            user=user
        ).values_list(
            'value'
        ).first()


FEATURE_FLAG_REPOSITORY = FeatureFlagRepository()
