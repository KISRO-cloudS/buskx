from django.contrib import admin
from .models import Profile, Follow, Comment, Activity, SupportCampaign, Love, CampaignView, Chat, Message
from .models import  Brainstorming,  AffiliateLink
from .models import ActivityLove, ActivityComment,CampaignProduct
from .models import Notification,Report,NotInterested 
from django.contrib import messages
from .models import Surah, QuranVerse

from .models import Adhkar
from .models import Hadith

from .models import PlatformFund
from .models import Subscriber

from .models import AffiliateLibrary, AffiliateNewsSource
from .models import NativeAd

from .models import Campaign, CampaignFund
from .models import Donation  # Adjust the import based on your project structure

from .models import  ChangemakerAward,UserVerification

from django.contrib import admin
from .models import UserVerification, Notification

class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'submission_date')
    search_fields = ('user__username', 'document_type', 'status')
    
    def save_model(self, request, obj, form, change):
        """Override save_model to notify the user when their verification status changes."""
        super().save_model(request, obj, form, change)  # Save the instance

        # Check if the verification has been approved or rejected
        if obj.status == 'Rejected':
            message = f"Your verification for {obj.document_type} has been rejected. Reason: {obj.rejection_reason}."
            Notification.objects.create(user=obj.user, message=message)
        elif obj.status == 'Approved':
            message = f"Your verification for {obj.document_type} has been approved."
            Notification.objects.create(user=obj.user, message=message)

admin.site.register(UserVerification, UserVerificationAdmin)








class ChangemakerAwardAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'award', 'timestamp')
    search_fields = ('user__username', 'campaign__title', 'award')
    list_filter = ('award', 'timestamp')
    ordering = ('-timestamp',)

admin.site.register(ChangemakerAward, ChangemakerAwardAdmin)




class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'amount', 'donor_name', 'transaction_id')  # Exclude created_at
    search_fields = ('donor_name', 'transaction_id')  # Enable search by donor name and transaction ID
    list_filter = ('campaign',)  # Allow filtering by campaign

    # Optional: Add any additional configurations like ordering, etc.
    ordering = ('-id',)  # Order by ID, descending

admin.site.register(Donation, DonationAdmin) 

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'timestamp')
    search_fields = ('user__user__username', 'title')
    list_filter = ('timestamp',)

    # Add the inline for CampaignFund
    class CampaignFundInline(admin.StackedInline):
        model = CampaignFund
        extra = 1  # Number of empty forms to display

    inlines = [CampaignFundInline]

# Register the CampaignFund model separately if you want to manage it independently
@admin.register(CampaignFund)
class CampaignFundAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'target_amount', 'amount_raised')
    search_fields = ('campaign__title', )




@admin.register(NativeAd)
class NativeAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'sponsored_by', 'link')  # Customize displayed fields in the list
    search_fields = ('title', 'sponsored_by')  # Add fields for search functionality
    list_filter = ('sponsored_by',)  # Add filters for sponsored_by field
    # You can customize further with fields, list_per_page, etc.



admin.site.register(AffiliateLibrary)
admin.site.register(AffiliateNewsSource)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

admin.site.register(Subscriber, SubscriberAdmin)



@admin.register(PlatformFund)
class PlatformFundAdmin(admin.ModelAdmin):
    list_display = ('donation_link',)






class HadithAdmin(admin.ModelAdmin):
    list_display = ('id', 'narrator', 'reference', 'authenticity')
    search_fields = ('narrator', 'reference', 'authenticity')
    list_filter = ('authenticity',)

admin.site.register(Hadith, HadithAdmin)





@admin.register(Adhkar)
class AdhkarAdmin(admin.ModelAdmin):
    list_display = ('type', 'text', 'translation', 'reference')
    search_fields = ('type', 'text', 'translation', 'reference')








@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ('name', 'surah_number')
    search_fields = ('name',)

@admin.register(QuranVerse)
class QuranVerseAdmin(admin.ModelAdmin):
    list_display = ('surah', 'verse_number', 'description')  # Include description here
    search_fields = ('surah__name', 'verse_text', 'translation', 'description')  # Include description here
    list_filter = ('surah',)


from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'is_verified')  # Added 'is_verified' for display
    search_fields = ('user__username', 'bio', 'location')  # Search functionality
    readonly_fields = ('user',)  # Make user field read-only

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete permission in admin

    def has_add_permission(self, request):
        return False  # Disable add permission in admin

    actions = ['verify_users']  # Add custom action for verifying users

    def verify_users(self, request, queryset):
        # Verify selected users
        for profile in queryset:
            profile.is_verified = True
            profile.save()
        self.message_user(request, "Selected profiles have been verified.")

    verify_users.short_description = "Verify selected users"  # Action description

# Register the Profile model with the customized ProfileAdmin
admin.site.register(Profile, ProfileAdmin)




class ReportAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'reported_by', 'reason', 'timestamp')
    search_fields = ('campaign__title', 'reported_by__user__username', 'reason')
    list_filter = ('reason', 'timestamp')
    
    actions = ['delete_reported_campaigns']

    def delete_reported_campaigns(self, request, queryset):
        for report in queryset:
            campaign = report.campaign
            campaign_title = campaign.title
            campaign.delete()
            messages.success(request, f'The campaign "{campaign_title}" has been deleted.')

    delete_reported_campaigns.short_description = "Delete selected campaigns"

admin.site.register(Report, ReportAdmin)



# Register the Notification model
admin.site.register(Notification)
admin.site.register(NotInterested)

admin.site.register(AffiliateLink)

admin.site.register(ActivityLove)
admin.site.register(ActivityComment)





@admin.register(CampaignProduct)
class CampaignProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'price', 'stock_quantity', 'is_active')
    list_filter = ('campaign', 'is_active')
    search_fields = ('name', 'description', 'sku')
    list_editable = ('price', 'stock_quantity', 'is_active')







@admin.register(Brainstorming)
class BrainstormingAdmin(admin.ModelAdmin):
    list_display = ('idea', 'supporter', 'campaign')
    search_fields = ('supporter__username', 'campaign__title')
    list_filter = ('campaign',)











@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')
    search_fields = ('follower__username', 'followed__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'timestamp')
    search_fields = ('user__user__username', 'campaign__title', 'text')
    list_filter = ('timestamp',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'timestamp')
    search_fields = ('campaign__title', 'content')
    list_filter = ('timestamp',)




class SupportCampaignAdmin(admin.ModelAdmin):
    list_display = ['user', 'campaign', 'donate_monetary_visible', 'attend_event_visible', 'brainstorm_idea_visible','campaign_product_visible']






@admin.register(Love)
class LoveAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign')
    search_fields = ('user__username', 'campaign__title')

@admin.register(CampaignView)
class CampaignViewAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'user', 'timestamp')  # Remove 'time_spent'
    search_fields = ('campaign__title', 'user__username')
    list_filter = ('timestamp',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants',)  # Allows selecting multiple participants easily
    list_display = ('id', 'created_at')
    search_fields = ('id',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'timestamp', 'content')
    search_fields = ('chat__id', 'sender__username', 'content')
    list_filter = ('timestamp',)


class CampaignInline(admin.TabularInline):
    model = Campaign
    extra = 0  # No extra empty rows

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'followers_count', 'is_verified', 'is_changemaker']
    search_fields = ['user__username', 'location']
    list_filter = ['is_verified']
    inlines = [CampaignInline]

    def is_changemaker(self, obj):
        return any(campaign.is_changemaker for campaign in obj.user_campaigns.all())
    is_changemaker.boolean = True
    is_changemaker.short_description = 'Changemaker'