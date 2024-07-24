# leave/manager.py
import mongoengine as me
from datetime import datetime

class LeaveManager:
    def all_pending_leaves(self):
        '''
        Gets all pending leaves
        '''
        return Leave.objects(status='pending').order_by('-created')

    def all_cancel_leaves(self):
        '''
        Gets all cancelled leaves
        '''
        return Leave.objects(status='cancelled').order_by('-created')

    def all_rejected_leaves(self):
        '''
        Gets all rejected leaves
        '''
        return Leave.objects(status='rejected').order_by('-created')

    def all_approved_leaves(self):
        '''
        Gets all approved leaves
        '''
        return Leave.objects(status='approved')

    def current_year_leaves(self):
        '''
        Returns all leaves in the current year
        '''
        current_year = datetime.now().year
        return Leave.objects(startdate__year=current_year)
