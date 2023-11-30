from django import forms
from core.models import ProductReview,Category,Vendor

# review form
class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        

# coupon form
class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your coupon code"}))

