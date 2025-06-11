#-------------------------------------------------------------------------------
# Name:        views.py
# Purpose:     Define viewsets to manage APIs for JobSite, JobApplication, and ApplicationTimeline.
#
# Author:      rafaelfullstackdeveloper
#
# Created:     31/05/2025
# Copyright:   (c) rafaelfullstackdeveloper 2025
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import JobSite, JobApplication, ApplicationTimeline
from .serializers import JobSiteSerializer, JobApplicationSerializer, ApplicationTimelineSerializer
class JobSiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations and custom actions for the JobSite model.

    Attributes:
        queryset        : All available JobSite objects.
        serializer_class: Serializer used to convert JobSite to JSON.
    """
    queryset        = JobSite.objects.all()         # Defines the default queryset for all operations.
    serializer_class= JobSiteSerializer             # Serializer used for API responses.

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """
        Custom action that returns general statistics about job sites.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON containing the total sites, visited sites, completed sites, and pending sites.
        """
        total_sites      = JobSite.objects.count()                        # Counts the total number of sites.
        visited_sites    = JobSite.objects.filter(visited=True).count()   # Counts sites marked as visited.
        completed_sites  = JobSite.objects.filter(is_completed=True).count() # Counts sites marked as completed.
        pending_sites    = total_sites - visited_sites                    # Calculates pending (not visited) sites.

        return Response({
            'total_sites'     : total_sites,
            'visited_sites'   : visited_sites,
            'completed_sites' : completed_sites,
            'pending_sites'   : pending_sites,
        })

    @action(detail=True, methods=['post'])
    def mark_visited(self, request, pk=None):
        """
        Custom action to mark a site as visited.

        Args:
            request: HTTP request object.
            pk     : Primary key of the site to be marked (provided by the URL).

        Returns:
            Response: JSON confirming the site was marked as visited.
        """
        site         = self.get_object()    # Gets the JobSite object based on pk.
        site.visited = True                 # Marks the site as visited.
        site.save()                         # Saves changes to the database.
        return Response({'status': 'marked as visited'})

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Custom action to mark a site as completed.

        Args:
            request: HTTP request object.
            pk     : Primary key of the site to be marked (provided by the URL).

        Returns:
            Response: JSON confirming the site was marked as completed.
        """
        site              = self.get_object()  # Gets the JobSite object based on pk.
        site.is_completed = True               # Marks the site as completed.
        site.save()                            # Saves changes to the database.
        return Response({'status': 'marked as completed'})

class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations and custom actions for the JobApplication model.

    Attributes:
        queryset        : All available JobApplication objects.
        serializer_class: Serializer used to convert JobApplication to JSON.
    """
    queryset        = JobApplication.objects.all()     # Defines the default queryset for all operations.
    serializer_class= JobApplicationSerializer         # Serializer used for API responses.

    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """
        Custom action that returns a list of non-archived applications, ordered by application date.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON with serialized application data.
        """
        applications = JobApplication.objects.filter(is_archived=False).order_by('-applied_date')  # Filters non-archived applications and orders by descending date.
        serializer   = self.get_serializer(applications, many=True)                                # Serializes the list of applications.
        return Response(serializer.data)  # Returns the serialized data.

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
        Custom action to archive an application.

        Args:
            request: HTTP request object.
            pk     : Primary key of the application to be archived (provided by the URL).

        Returns:
            Response: JSON confirming the application was archived.
        """
        application             = self.get_object()  # Gets the JobApplication object based on pk.
        application.is_archived = True               # Marks the application as archived.
        application.save()                           # Saves changes to the database.
        return Response({'status': 'archived'})

    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """
        Custom action to unarchive an application.

        Args:
            request: HTTP request object.
            pk     : Primary key of the application to be unarchived (provided by the URL).

        Returns:
            Response: JSON confirming the application was unarchived.
        """
        application             = self.get_object()  # Gets the JobApplication object based on pk.
        application.is_archived = False              # Marks the application as not archived.
        application.save()                           # Saves changes to the database.
        return Response({'status': 'unarchived'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Custom action that returns statistics about the applications.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON with total applications, count by status, and number of archived applications.
        """
        total     = JobApplication.objects.count()  # Counts the total number of applications.
        by_status = JobApplication.objects.values('status').annotate(count=Count('status'))  # Groups applications by status and counts each group.
        archived  = JobApplication.objects.filter(is_archived=True).count()  # Counts archived applications.

        return Response({
            'total_applications': total,
            'by_status'         : by_status,
            'archived'          : archived,
        })

class ApplicationTimelineViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations for the ApplicationTimeline model.

    Attributes:
        queryset        : All available ApplicationTimeline objects.
        serializer_class: Serializer used to convert ApplicationTimeline to JSON.
    """
    queryset        = ApplicationTimeline.objects.all()      # Defines the default queryset for all operations.
    serializer_class= ApplicationTimelineSerializer          # Serializer used for API responses.
