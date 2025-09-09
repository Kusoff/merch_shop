from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Users, EmailVerification, Category, Product, Product_Images, Characteristic, Basket, \
    Discount_For_Product_Category, Comments


# ---------------- Users -----------------
@admin.register(Users)
class UsersAdmin(BaseUserAdmin):
    model = Users
    list_display = ('username', 'email', 'phone', 'is_verified_email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_verified_email')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone', 'slug', 'birthday', 'address', 'user_photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


# ---------------- Email Verification -----------------
@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created', 'expiration', 'is_expired')
    readonly_fields = ('created',)
    search_fields = ('user__username', 'user__email', 'code')


# ---------------- Category -----------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')


# ---------------- Product Images -----------------
@admin.register(Product_Images)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('img_name', 'img_tag', 'first_img', 'slug')
    search_fields = ('img_name', 'slug')

    def img_tag(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="50" />'.format(obj.img.url))
        return "-"

    img_tag.short_description = "Preview"


# ---------------- Product -----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'first_price', 'discount', 'last_price', 'category', 'stock', 'available', 'created', 'updated')
    list_filter = ('available', 'category')
    search_fields = ('name', 'slug', 'category__name')
    filter_horizontal = ('product_photos', 'product_characteristic')


# ---------------- Characteristic -----------------
@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('characteristic_name', 'value')
    search_fields = ('characteristic_name', 'value')


# ---------------- Basket -----------------
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'sum', 'created_timestamp')
    search_fields = ('user__username', 'product__name')


# ---------------- Discount For Product Category -----------------
@admin.register(Discount_For_Product_Category)
class DiscountCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'discount_percentage', 'discount_start_date', 'discount_end_date', 'slug')
    search_fields = ('category__name', 'slug')


# ---------------- Comments -----------------
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created')
    search_fields = ('user__username', 'product__name', 'text')
    list_filter = ('rating',)
