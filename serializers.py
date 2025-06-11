#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Define serializers to convert JobSite, JobApplication, and ApplicationTimeline models to JSON.
#
# Author:      rafaelfullstackdeveloper
#
# Created:     31/05/2025
# Copyright:   (c) rafaelfullstackdeveloper 2025
# Licence:     GNU
#-------------------------------------------------------------------------------
# This file defines serializers for the JobSite, JobApplication, and ApplicationTimeline models.
# The serializers convert model instances into JSON representations for use in REST APIs.
# Uses Django REST Framework to facilitate serialization and deserialization of data.

from rest_framework import serializers
from .models import JobSite, JobApplication, ApplicationTimeline
class JobSiteSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobSite model, converts model instances to and from JSON representations.
    Attributes:
        applications_count (SerializerMethodField): Computed field that returns the number of applications associated with the site.
    """

    applications_count = serializers.SerializerMethodField()

    class Meta:
        model  = JobSite    # Model associated with the serializer.
        fields = '__all__'  # Includes all fields from the JobSite model in the serialization.

    def get_applications_count(self, obj):
        """
        Calculates the number of applications associated with a JobSite.

        Args:
            obj (JobSite): Instance of the JobSite model.

        Returns:
            int: Number of applications linked to the site.
        """
        return obj.applications.count()


class ApplicationTimelineSerializer(serializers.ModelSerializer):
    """
    Serializer for the ApplicationTimeline model, converts timeline events to JSON representations.
    """

    class Meta:
        model  = ApplicationTimeline  # Model associated with the serializer.
        fields = '__all__'            # Includes all fields from the ApplicationTimeline model in the serialization.


class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobApplication model, converts applications to and from JSON representations.

    Attributes:
        timeline (ApplicationTimelineSerializer): Nested field that includes the timeline associated with the application (read-only).
        job_site_name (CharField): Field that extracts the name of the associated job site (read-only).
    """

    timeline      = ApplicationTimelineSerializer(many=True, read_only=True)      # Includes the list of timeline events.
    job_site_name = serializers.CharField(source='job_site.name', read_only=True) # Name of the associated job site.

    class Meta:
        model  = JobApplication  # Model associated with the serializer.
        fields = '__all__'       # Includes all fields from the JobApplication model in the serialization.
