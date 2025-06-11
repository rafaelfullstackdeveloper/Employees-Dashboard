#-------------------------------------------------------------------------------
# Name:        models.py
# Purpose:     Define data models for managing job sites, applications, and application timelines.
#
# Author:      rafaelfullstackdeveloper
#
# Created:     31/05/2025
# Copyright:   (c) rafaelfullstackdeveloper 2025
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User

class JobSite(models.Model):
    """
    Model representing a job board or job opportunity platform.

    Attributes:
        name         (CharField)     : Name of the job site.
        url          (URLField)      : URL of the site.
        site_type    (CharField)     : Type of site (e.g., job_board, company, challenge, freelance).
        country      (CharField)     : Country of origin or focus of the site.
        language     (CharField)     : Main language of the site.
        work_area    (CharField)     : Main work area of the site (e.g., technology, design).
        description  (TextField)     : Detailed description of the site (optional).
        is_completed (BooleanField)  : Indicates if the site has been fully explored or analyzed.
        visited      (BooleanField)  : Indicates if the site has been visited.
        created_at   (DateTimeField) : Record creation date.
        updated_at   (DateTimeField) : Last update date.
    """

    SITE_TYPES = [
        ('job_board',   'Job Board'),
        ('company',     'Company Site'),
        ('challenge',   'Code Challenge'),
        ('freelance',   'Freelance'),
    ]

    COUNTRIES = [
        ('BR',      'Brazil'),
        ('US',      'United States'),
        ('CA',      'Canada'),
        ('UK',      'United Kingdom'),
        ('DE',      'Germany'),
        ('FR',      'France'),
        ('ES',      'Spain'),
        ('PT',      'Portugal'),
        ('OTHER',   'Other'),
    ]

    LANGUAGES = [
        ('pt',      'Portuguese'),
        ('en',      'English'),
        ('es',      'Spanish'),
        ('fr',      'French'),
        ('de',      'German'),
        ('other',   'Other'),
    ]

    WORK_AREAS = [
        ('tech',        'Technology'),
        ('design',      'Design'),
        ('marketing',   'Marketing'),
        ('sales',       'Sales'),
        ('finance',     'Finance'),
        ('hr',          'Human Resources'),
        ('general',     'General'),
    ]

    name         = models.CharField( max_length=200, help_text="Job site name." )
    url          = models.URLField( help_text="Job site URL." )
    site_type    = models.CharField( max_length=20, choices=SITE_TYPES, help_text="Type of site." )
    country      = models.CharField( max_length=10, choices=COUNTRIES, help_text="Country of origin or focus." )
    language     = models.CharField( max_length=10, choices=LANGUAGES, help_text="Main language of the site." )
    work_area    = models.CharField( max_length=20, choices=WORK_AREAS, help_text="Main work area of the site." )
    description  = models.TextField( blank=True, help_text="Detailed description of the site (optional)." )
    is_completed = models.BooleanField( default=False, help_text="Indicates if the site has been fully explored." )
    visited      = models.BooleanField( default=False, help_text="Indicates if the site has been visited." )
    created_at   = models.DateTimeField( auto_now_add=True, help_text="Record creation date." )
    updated_at   = models.DateTimeField( auto_now=True, help_text="Last update date." )

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: Site name.
        """
        return self.name

    class Meta:
        ordering            = ['-created_at']           # Order by creation date descending
        verbose_name        = "Job Site"                # Singular name for admin
        verbose_name_plural = "Job Sites"               # Plural name for admin

class JobApplication(models.Model):
    """
    Model representing a job application.

    Attributes:
        job_site      (ForeignKey):    Reference to the related job site.
        position      (CharField):     Job title.
        company       (CharField):     Name of the company offering the job.
        job_url       (URLField):      Job URL (optional).
        description   (TextField):     Job description (optional).
        salary_range  (CharField):     Salary range (optional).
        status        (CharField):     Application status (e.g., applied, interview, rejected).
        applied_date  (DateTimeField): Application submission date.
        notes         (TextField):     Additional notes about the application (optional).
        is_archived   (BooleanField):  Indicates if the application is archived.
    """

    STATUS_CHOICES = [
        ('applied',   'Applied'),
        ('interview', 'Interview'),
        ('rejected',  'Rejected'),
        ('accepted',  'Accepted'),
        ('pending',   'Pending'),
        ('archived',  'Archived'),
    ]

    job_site     = models.ForeignKey( JobSite, on_delete=models.CASCADE, related_name='applications', help_text="Related job site." )         # Reference to JobSite
    position     = models.CharField( max_length=200, help_text="Job title." )                                                                 # Job title
    company      = models.CharField( max_length=200, help_text="Company name." )                                                              # Company name
    job_url      = models.URLField( blank=True, help_text="Job URL (optional)." )                                                             # Optional job URL
    description  = models.TextField( blank=True, help_text="Job description (optional)." )                                                    # Optional job description
    salary_range = models.CharField( max_length=100, blank=True, help_text="Salary range (optional)." )                                       # Optional salary range
    status       = models.CharField( max_length=20, choices=STATUS_CHOICES, default='applied', help_text="Application status." )              # Application status
    applied_date = models.DateTimeField( auto_now_add=True, help_text="Application submission date." )                                        # Submission date
    notes        = models.TextField( blank=True, help_text="Additional notes about the application." )                                        # Optional notes
    is_archived  = models.BooleanField( default=False, help_text="Indicates if the application is archived." )                                # Archive flag

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: Job title and company name.
        """
        return f"{self.position} - {self.company}"

    class Meta:
        ordering            = ['-applied_date']           # Order by applied date descending
        verbose_name        = "Job Application"           # Singular name for admin
        verbose_name_plural = "Job Applications"          # Plural name for admin

class ApplicationTimeline(models.Model):
    """
    Model representing events in the timeline of a job application.

    Attributes:
        application (ForeignKey) : Reference to the related application.
        event_type  (CharField)  : Type of event (e.g., applied, interview_scheduled, rejected).
        title       (CharField)  : Event title.
        description (TextField)  : Detailed event description (optional).
        date        (DateTimeField): Event date.
    """

    EVENT_TYPES = [
        ('applied',             'Application Sent'),        # Application was sent
        ('viewed',              'Resume Viewed'),           # Resume was viewed by employer
        ('interview_scheduled', 'Interview Scheduled'),     # Interview was scheduled
        ('interview_completed', 'Interview Completed'),     # Interview was completed
        ('feedback',            'Feedback Received'),       # Feedback received from employer
        ('rejected',            'Rejected'),                # Application was rejected
        ('accepted',            'Accepted'),                # Application was accepted
        ('other',               'Other'),                   # Other event
    ]

    application = models.ForeignKey( JobApplication, on_delete=models.CASCADE, related_name='timeline', help_text="Related application." )          # Reference to JobApplication
    event_type  = models.CharField( max_length=30, choices=EVENT_TYPES, help_text="Type of event in the timeline." )                                # Type of event
    title       = models.CharField( max_length=200, help_text="Event title." )                                                                      # Event title
    description = models.TextField( blank=True, help_text="Detailed event description (optional)." )                                                # Optional event description
    date        = models.DateTimeField( auto_now_add=True, help_text="Event date." )                                                                # Event date

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: Job title and event title.
        """
        return f"{self.application.position} - {self.title}"

    class Meta:
        ordering            = ['-date']           # Order by event date descending
        verbose_name        = "Timeline Event"    # Singular name for admin
        verbose_name_plural = "Timeline Events"   # Plural name for admin