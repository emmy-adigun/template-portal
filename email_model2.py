import requests
import streamlit as st
import time
import re
from streamlit_quill import st_quill

# Pre-defined HTML email templates with color placeholders
EMAIL_TEMPLATES = {
    "Modern Corporate": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Corporate Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table width="600" border="0" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="border: 1px solid #dddddd;">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 30px 20px; background-color: [HEADER_COLOR]; color: [HEADER_TEXT_COLOR];">
                            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">[COMPANY_NAME]</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px;">[EMAIL_TITLE]</p>
                        </td>
                    </tr>
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: [TEXT_COLOR]; margin-top: 0;">[CONTENT_HEADING]</h2>
                            <p style="font-size: 16px; color: [TEXT_COLOR]; line-height: 1.6;">[MAIN_CONTENT]</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="[CTA_LINK]" style="background-color: [BUTTON_COLOR]; color: [BUTTON_TEXT_COLOR]; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">[CTA_TEXT]</a>
                            </div>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 20px; background-color: #ecf0f1; color: #7f8c8d; font-size: 12px;">
                            <p style="margin: 0;">&copy; 2024 [COMPANY_NAME]. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """,

    "E-commerce Promotional": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Promotional Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#f8f9fa">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table width="600" border="0" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 30px 20px; background-color: [HEADER_COLOR]; color: [HEADER_TEXT_COLOR];">
                            <h1 style="margin: 0; font-size: 32px; font-weight: bold;">[PROMOTION_TITLE]</h1>
                            <p style="margin: 10px 0 0 0; font-size: 18px;">[PROMOTION_SUBTITLE]</p>
                        </td>
                    </tr>
                    <!-- Hero Image -->
                    <tr>
                        <td align="center" style="padding: 20px;">
                            <img src="[HERO_IMAGE]" alt="Promotional Banner" width="560" style="display: block; max-width: 560px; border-radius: 5px;">
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px;">
                            <h2 style="color: [TEXT_COLOR]; margin-top: 0;">[CONTENT_HEADING]</h2>
                            <p style="font-size: 16px; color: [TEXT_COLOR]; line-height: 1.6;">[MAIN_CONTENT]</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="[SHOP_LINK]" style="background-color: [BUTTON_COLOR]; color: [BUTTON_TEXT_COLOR]; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; display: inline-block;">[CTA_BUTTON]</a>
                            </div>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 20px; background-color: #343a40; color: #ffffff; font-size: 12px;">
                            <p style="margin: 0;">Shop now and enjoy great deals! | <a href="[UNSUBSCRIBE_LINK]" style="color: #ffffff;">Unsubscribe</a></p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """,

    "Newsletter": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
</head>
<body style="margin: 0; padding: 0; font-family: Georgia, serif; background-color: #fdf6e3;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#fdf6e3">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table width="600" border="0" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="border: 2px solid #d4a574;">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 30px 20px; background-color: [HEADER_COLOR]; color: [HEADER_TEXT_COLOR];">
                            <h1 style="margin: 0; font-size: 28px; font-family: 'Times New Roman', serif;">[NEWSLETTER_TITLE]</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px; font-style: italic;">[NEWSLETTER_DATE]</p>
                        </td>
                    </tr>
                    <!-- Featured Article -->
                    <tr>
                        <td style="padding: 30px;">
                            <h2 style="color: [TEXT_COLOR]; border-bottom: 2px solid #d4a574; padding-bottom: 10px;">[FEATURED_HEADING]</h2>
                            <p style="font-size: 16px; color: [TEXT_COLOR]; line-height: 1.8;">[FEATURED_CONTENT]</p>
                        </td>
                    </tr>
                    <!-- Secondary Content -->
                    <tr>
                        <td style="padding: 0 30px 30px 30px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="48%" style="padding: 15px; background-color: #f9f9f9; border: 1px solid #eeeeee;">
                                        <h3 style="color: [TEXT_COLOR]; margin-top: 0;">[SECTION1_HEADING]</h3>
                                        <p style="font-size: 14px; color: [TEXT_COLOR];">[SECTION1_CONTENT]</p>
                                    </td>
                                    <td width="4%"></td>
                                    <td width="48%" style="padding: 15px; background-color: #f9f9f9; border: 1px solid #eeeeee;">
                                        <h3 style="color: [TEXT_COLOR]; margin-top: 0;">[SECTION2_HEADING]</h3>
                                        <p style="font-size: 14px; color: [TEXT_COLOR];">[SECTION2_CONTENT]</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 20px; background-color: #f5f5f5; color: #666666; font-size: 12px;">
                            <p style="margin: 0;">[NEWSLETTER_FOOTER]</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """,

    "Minimal Modern": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #ffffff;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#ffffff">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table width="500" border="0" cellpadding="0" cellspacing="0">
                    <!-- Logo/Header -->
                    <tr>
                        <td align="center" style="padding-bottom: 30px;">
                            <h1 style="margin: 0; font-size: 24px; color: [TEXT_COLOR]; font-weight: 300;">[BRAND_NAME]</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 0; border-top: 1px solid #eeeeee; border-bottom: 1px solid #eeeeee;">
                            <h2 style="color: [TEXT_COLOR]; font-size: 20px; font-weight: 400; margin-top: 0;">[CONTENT_TITLE]</h2>
                            <p style="font-size: 16px; color: [TEXT_COLOR]; line-height: 1.6; margin-bottom: 30px;">[MAIN_CONTENT]</p>
                            <a href="[ACTION_LINK]" style="color: [BUTTON_COLOR]; text-decoration: none; font-size: 16px;">[ACTION_TEXT] →</a>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 30px 0; color: #999999; font-size: 12px;">
                            <p style="margin: 0;">[FOOTER_TEXT]</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """
}

st.markdown("""
    <style>
        .ql-editor {
            min-height: 150px !important;
            font-family: Arial, sans-serif !important;
        }
        .ql-toolbar {
            border-radius: 5px 5px 0 0 !important;
            background-color: #f8f9fa !important;
        }
        .ql-container {
            border-radius: 0 0 5px 5px !important;
        }
        .color-preview-box {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 10px;
            border: 1px solid #ddd;
            vertical-align: middle;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
    </style>
""", unsafe_allow_html=True)


def replace_template_content(template, content_data, colors):
    """Replace placeholder content and colors in the template"""
    replaced_template = template

    # First replace colors
    for color_key, color_value in colors.items():
        replaced_template = replaced_template.replace(f"[{color_key}]", color_value)

    # Then replace content
    for placeholder, content in content_data.items():
        if content:
            if placeholder == "MAIN_CONTENT" or "CONTENT" in placeholder:
                replaced_template = replaced_template.replace(f"[{placeholder}]", str(content))
            else:
                clean_content = re.sub('<[^<]+?>', '', str(content))
                replaced_template = replaced_template.replace(f"[{placeholder}]", clean_content)

    # Remove any remaining placeholders
    remaining_placeholders = re.findall(r'\[(.*?)\]', replaced_template)
    for placeholder in remaining_placeholders:
        replaced_template = replaced_template.replace(f"[{placeholder}]", "")

    return replaced_template


def quick_email_template(prompt, content_text, image_links, api_key):
    """
    Generate email templates with uploaded content and image links
    """
    url = "https://ai-models-backend.k9.isw.la/v1/completions"
    headers = {"Authorization": f"Bearer {api_key}"}

    email_prompt = f"""
Create a complete HTML email template with table layout and inline CSS based on these requirements:

EMAIL PURPOSE: {prompt}

CONTENT TO INCLUDE: {content_text}

IMAGE LINKS TO USE: {', '.join(image_links) if image_links else 'No specific images provided'}

REQUIREMENTS:
- Use table-based layout with inline CSS only
- Maximum width: 600px
- Mobile-responsive design
- Include proper HTML structure with doctype, html, head, body tags
- Use web-safe fonts (Arial, Helvetica, Georgia)
- Ensure all tags are properly closed
- Make it professional and visually appealing
- Include placeholders for images if links are provided

Generate complete HTML code starting with <!DOCTYPE html>:
"""

    data = {
        "model": "PetrosStav/gemma3-tools:27b",
        "prompt": email_prompt,
        "max_tokens": 2000,
        "temperature": 0.3,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        html_content = result["choices"][0]["text"].strip()

        return ensure_complete_html(html_content)

    except Exception as e:
        return f"Error: {str(e)}"


def ensure_complete_html(html_content):
    """
    Ensure the HTML template has complete structure
    """
    if not html_content.strip().startswith('<!DOCTYPE html>'):
        html_content = '<!DOCTYPE html>\n' + html_content

    if not html_content.strip().endswith('</html>'):
        if '</body>' not in html_content:
            html_content += '\n</body>'
        html_content += '\n</html>'

    return html_content


def html_to_plain_text(html_content):
    """Convert HTML to plain text for display in simple fields"""
    if not html_content:
        return ""

    text = re.sub(r'<[^>]+>', '', html_content)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    return text.strip()


def get_default_colors(template_name):
    """Get default colors for each template"""
    defaults = {
        "Modern Corporate": {
            "HEADER_COLOR": "#2c3e50",
            "HEADER_TEXT_COLOR": "#ffffff",
            "BUTTON_COLOR": "#e74c3c",
            "BUTTON_TEXT_COLOR": "#ffffff",
            "TEXT_COLOR": "#333333"
        },
        "E-commerce Promotional": {
            "HEADER_COLOR": "#667eea",
            "HEADER_TEXT_COLOR": "#ffffff",
            "BUTTON_COLOR": "#28a745",
            "BUTTON_TEXT_COLOR": "#ffffff",
            "TEXT_COLOR": "#333333"
        },
        "Newsletter": {
            "HEADER_COLOR": "#8b4513",
            "HEADER_TEXT_COLOR": "#ffffff",
            "BUTTON_COLOR": "#8b4513",
            "BUTTON_TEXT_COLOR": "#ffffff",
            "TEXT_COLOR": "#333333"
        },
        "Minimal Modern": {
            "HEADER_COLOR": "#333333",
            "HEADER_TEXT_COLOR": "#333333",
            "BUTTON_COLOR": "#007bff",
            "BUTTON_TEXT_COLOR": "#007bff",
            "TEXT_COLOR": "#333333"
        }
    }
    return defaults.get(template_name, defaults["Modern Corporate"])


def get_template_preview(template_name, colors=None, content_data=None):
    """Generate a preview of the template with current colors and sample content"""
    if colors is None:
        colors = get_default_colors(template_name)

    if content_data is None:
        # Use sample content for preview
        content_data = {
            "COMPANY_NAME": "Your Company",
            "EMAIL_TITLE": "Important Announcement",
            "CONTENT_HEADING": "Latest Updates",
            "MAIN_CONTENT": "This is where your content will appear...",
            "CTA_TEXT": "Learn More",
            "CTA_LINK": "#",
            "PROMOTION_TITLE": "Special Offer!",
            "PROMOTION_SUBTITLE": "Limited Time Only",
            "HERO_IMAGE": "https://via.placeholder.com/560x200/667eea/ffffff?text=Promotional+Banner",
            "SHOP_LINK": "#",
            "UNSUBSCRIBE_LINK": "#",
            "CTA_BUTTON": "Shop Now",
            "NEWSLETTER_TITLE": "Monthly Newsletter",
            "NEWSLETTER_DATE": "January 2024",
            "FEATURED_HEADING": "Featured Story",
            "FEATURED_CONTENT": "This month's featured content...",
            "SECTION1_HEADING": "Latest News",
            "SECTION1_CONTENT": "Recent updates and announcements...",
            "SECTION2_HEADING": "Upcoming Events",
            "SECTION2_CONTENT": "Events happening soon...",
            "NEWSLETTER_FOOTER": "Thank you for reading!",
            "BRAND_NAME": "Your Brand",
            "CONTENT_TITLE": "Important Update",
            "ACTION_TEXT": "Learn more",
            "ACTION_LINK": "#",
            "FOOTER_TEXT": "Sent with ❤️ from Your Brand"
        }

    template = EMAIL_TEMPLATES[template_name]
    return replace_template_content(template, content_data, colors)


def main():
    st.set_page_config(
        page_title="📧 Smart Email Template Generator",
        page_icon="✉️",
        layout="wide"
    )

    st.title("🎨 Email Template Generator")
    st.markdown("**Create beautiful emails with simple color customization**")

    # Sidebar for API key
    with st.sidebar:
        st.header("🔐 Configuration")
        api_key = st.text_input("Enter your API Key", type="password",
                                help="Required for AI template generation")

        st.header("🎯 Quick Actions")
        if st.button("🔄 Reset All", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎨 Template Selection")

        # Template selection method
        template_method = st.radio(
            "Choose your approach:",
            ["📁 Use Pre-built Template", "🤖 Generate with AI"],
            horizontal=True
        )

        if template_method == "📁 Use Pre-built Template":
            # Template selection
            selected_template = st.selectbox(
                "Choose a template:",
                list(EMAIL_TEMPLATES.keys()),
                help="Select a pre-designed email template"
            )

            if selected_template:
                # Initialize colors in session state
                if 'colors' not in st.session_state or st.session_state.get('last_template') != selected_template:
                    st.session_state.colors = get_default_colors(selected_template)
                    st.session_state.last_template = selected_template

                st.success(f"✅ Selected: {selected_template}")

                # LIVE PREVIEW WITH TABS
                st.subheader("👀 Template Preview")

                # Create tabs for Original and Custom Preview
                preview_tab1, preview_tab2 = st.tabs(["🎨 Custom Preview", "📄 Original Template"])

                with preview_tab1:
                    # Generate preview with current colors
                    preview_html = get_template_preview(selected_template, st.session_state.colors)
                    st.components.v1.html(preview_html, height=400, scrolling=True)
                    st.caption("Live preview with your selected colors")

                with preview_tab2:
                    # Show original template
                    original_html = get_template_preview(selected_template, get_default_colors(selected_template))
                    st.components.v1.html(original_html, height=400, scrolling=True)
                    st.caption("Original template with default colors")

                # SIMPLE COLOR CUSTOMIZATION SECTION
                st.subheader("🎨 Quick Color Customization")

                col_a, col_b = st.columns(2)

                with col_a:
                    # Header Color
                    header_col = st.color_picker(
                        "Header Background",
                        st.session_state.colors["HEADER_COLOR"],
                        key="header_color_picker"
                    )
                    st.session_state.colors["HEADER_COLOR"] = header_col

                    # Header Text Color
                    header_text_col = st.color_picker(
                        "Header Text",
                        st.session_state.colors["HEADER_TEXT_COLOR"],
                        key="header_text_color_picker"
                    )
                    st.session_state.colors["HEADER_TEXT_COLOR"] = header_text_col

                with col_b:
                    # Button Color
                    button_col = st.color_picker(
                        "Button Color",
                        st.session_state.colors["BUTTON_COLOR"],
                        key="button_color_picker"
                    )
                    st.session_state.colors["BUTTON_COLOR"] = button_col

                    # Button Text Color
                    button_text_col = st.color_picker(
                        "Button Text",
                        st.session_state.colors["BUTTON_TEXT_COLOR"],
                        key="button_text_color_picker"
                    )
                    st.session_state.colors["BUTTON_TEXT_COLOR"] = button_text_col

                # Text Color
                text_col = st.color_picker(
                    "Text Color",
                    st.session_state.colors["TEXT_COLOR"],
                    key="text_color_picker"
                )
                st.session_state.colors["TEXT_COLOR"] = text_col

                # Show color preview
                st.caption("Current Colors:")
                preview_cols = st.columns(5)
                with preview_cols[0]:
                    st.markdown(
                        f'<div class="color-preview-box" style="background-color: {st.session_state.colors["HEADER_COLOR"]};"></div>Header',
                        unsafe_allow_html=True)
                with preview_cols[1]:
                    st.markdown(
                        f'<div class="color-preview-box" style="background-color: {st.session_state.colors["BUTTON_COLOR"]};"></div>Button',
                        unsafe_allow_html=True)
                with preview_cols[2]:
                    st.markdown(
                        f'<div class="color-preview-box" style="background-color: {st.session_state.colors["TEXT_COLOR"]};"></div>Text',
                        unsafe_allow_html=True)

                # Reset to defaults button
                if st.button("🔄 Reset Colors to Default", key="reset_colors"):
                    st.session_state.colors = get_default_colors(selected_template)
                    st.success("✅ Colors reset to defaults!")
                    st.rerun()

        else:  # AI Generation
            st.subheader("🤖 AI Template Generation")
            ai_prompt = st.text_input(
                "Describe the template you want:",
                placeholder="e.g., Modern corporate newsletter with blue theme",
                key="ai_prompt_input"
            )

        st.subheader("📝 Your Content")

        # Initialize content_data in session state
        if 'content_data' not in st.session_state:
            st.session_state.content_data = {}

        if template_method == "📁 Use Pre-built Template" and selected_template:
            # Dynamic content fields based on template
            content_data = {}

            # Common editor configuration
            editor_config = {
                "modules": {
                    "toolbar": [
                        ["bold", "italic", "underline"],
                        [{"list": "ordered"}, {"list": "bullet"}],
                        ["link"],
                        ["clean"]
                    ]
                },
                "placeholder": "Type your content here..."
            }

            if selected_template == "Modern Corporate":
                content_data["COMPANY_NAME"] = st.text_input("Company Name", "Your Company", key="company_name")
                content_data["EMAIL_TITLE"] = st.text_input("Email Title", "Important Announcement", key="email_title")
                content_data["CONTENT_HEADING"] = st.text_input("Content Heading", "Latest Updates",
                                                                key="content_heading")

                st.markdown("**Main Content**")
                main_content = st_quill(
                    value="<p>Share your important news and updates here...</p>",
                    html=True,
                    key="main_content_corporate",
                    toolbar=editor_config["modules"]["toolbar"],
                    placeholder=editor_config["placeholder"]
                )
                content_data["MAIN_CONTENT"] = main_content

                content_data["CTA_TEXT"] = st.text_input("Button Text", "Learn More", key="cta_text")
                content_data["CTA_LINK"] = st.text_input("Button Link", "#", key="cta_link")

            elif selected_template == "E-commerce Promotional":
                content_data["PROMOTION_TITLE"] = st.text_input("Promotion Title", "Special Offer!", key="promo_title")
                content_data["PROMOTION_SUBTITLE"] = st.text_input("Promotion Subtitle", "Limited Time Only",
                                                                   key="promo_subtitle")
                content_data["HERO_IMAGE"] = st.text_input("Hero Image URL", "https://via.placeholder.com/560x200",
                                                           key="hero_image")
                content_data["CONTENT_HEADING"] = st.text_input("Content Heading", "Don't Miss Out!",
                                                                key="content_heading_ecom")

                st.markdown("**Main Content**")
                main_content = st_quill(
                    value="<p>Describe your amazing offer here...</p>",
                    html=True,
                    key="main_content_ecommerce",
                    toolbar=editor_config["modules"]["toolbar"],
                    placeholder=editor_config["placeholder"]
                )
                content_data["MAIN_CONTENT"] = main_content

                content_data["CTA_BUTTON"] = st.text_input("Button Text", "Shop Now", key="cta_button")
                content_data["SHOP_LINK"] = st.text_input("Shop Link", "#", key="shop_link")
                content_data["UNSUBSCRIBE_LINK"] = st.text_input("Unsubscribe Link", "#", key="unsubscribe_link")

            elif selected_template == "Newsletter":
                content_data["NEWSLETTER_TITLE"] = st.text_input("Newsletter Title", "Monthly Newsletter",
                                                                 key="newsletter_title")
                content_data["NEWSLETTER_DATE"] = st.text_input("Date", "January 2024", key="newsletter_date")
                content_data["FEATURED_HEADING"] = st.text_input("Featured Heading", "Featured Story",
                                                                 key="featured_heading")

                st.markdown("**Featured Content**")
                featured_content = st_quill(
                    value="<p>Your main featured content...</p>",
                    html=True,
                    key="featured_content",
                    toolbar=editor_config["modules"]["toolbar"],
                    placeholder=editor_config["placeholder"]
                )
                content_data["FEATURED_CONTENT"] = featured_content

                content_data["SECTION1_HEADING"] = st.text_input("Section 1 Heading", "Latest News",
                                                                 key="section1_heading")
                st.markdown("**Section 1 Content**")
                section1_content = st_quill(
                    value="<p>First section content...</p>",
                    html=True,
                    key="section1_content",
                    toolbar=[
                        ["bold", "italic"],
                        [{"list": "bullet"}],
                        ["link"]
                    ],
                    placeholder="Section content..."
                )
                content_data["SECTION1_CONTENT"] = section1_content

                content_data["SECTION2_HEADING"] = st.text_input("Section 2 Heading", "Upcoming Events",
                                                                 key="section2_heading")
                st.markdown("**Section 2 Content**")
                section2_content = st_quill(
                    value="<p>Second section content...</p>",
                    html=True,
                    key="section2_content",
                    toolbar=[
                        ["bold", "italic"],
                        [{"list": "bullet"}],
                        ["link"]
                    ],
                    placeholder="Section content..."
                )
                content_data["SECTION2_CONTENT"] = section2_content

                content_data["NEWSLETTER_FOOTER"] = st.text_input("Footer Text", "Thank you for reading!",
                                                                  key="newsletter_footer")

            elif selected_template == "Minimal Modern":
                content_data["BRAND_NAME"] = st.text_input("Brand Name", "Your Brand", key="brand_name")
                content_data["CONTENT_TITLE"] = st.text_input("Content Title", "Important Update", key="content_title")

                st.markdown("**Main Content**")
                main_content = st_quill(
                    value="<p>Your concise message here...</p>",
                    html=True,
                    key="main_content_minimal",
                    toolbar=[
                        ["bold", "italic"],
                        ["clean"]
                    ],
                    placeholder="Keep it concise..."
                )
                content_data["MAIN_CONTENT"] = main_content

                content_data["ACTION_TEXT"] = st.text_input("Action Text", "Learn more", key="action_text")
                content_data["ACTION_LINK"] = st.text_input("Action Link", "#", key="action_link")
                content_data["FOOTER_TEXT"] = st.text_input("Footer Text", "Sent with ❤️ from Your Brand",
                                                            key="footer_text_minimal")

            # Store in session state
            st.session_state.content_data = content_data

        else:  # AI Generation content
            st.markdown("**Enter your email content:**")
            content_text = st_quill(
                value="",
                html=True,
                key="ai_content",
                toolbar=[
                    ["bold", "italic", "underline"],
                    [{"list": "ordered"}, {"list": "bullet"}],
                    ["link", "image"],
                    ["clean"]
                ],
                placeholder="Type or paste your content here..."
            )

            # Store in session state
            st.session_state.ai_content = content_text

            # Image links for AI generation
            st.subheader("🖼️ Image Links (Optional)")
            image_links = []
            for i in range(2):
                img_link = st.text_input(
                    f"Image Link {i + 1}",
                    placeholder="https://example.com/image.jpg",
                    key=f"ai_image_{i}"
                )
                if img_link.strip():
                    image_links.append(img_link.strip())

        # Generate/Apply button
        if template_method == "📁 Use Pre-built Template":
            button_label = "🪄 Apply Content & Colors"
        else:
            button_label = "🤖 Generate AI Template"

        if st.button(button_label, type="primary", use_container_width=True, key="generate_button"):
            if template_method == "📁 Use Pre-built Template":
                if selected_template:
                    # Replace content and colors in selected template
                    template = EMAIL_TEMPLATES[selected_template]
                    final_template = replace_template_content(template, st.session_state.content_data,
                                                              st.session_state.colors)
                    st.session_state.final_template = final_template
                    st.session_state.template_source = f"Pre-built: {selected_template}"
                    st.success("✅ Template generated with your colors and content!")
                else:
                    st.error("Please select a template")

            else:  # AI Generation
                if not api_key:
                    st.error("🔑 API key required for AI generation")
                elif not ai_prompt.strip():
                    st.error("💬 Please describe the template you want")
                else:
                    plain_content = html_to_plain_text(st.session_state.get('ai_content', ''))

                    with st.spinner("🤖 Generating your custom template..."):
                        final_template = quick_email_template(ai_prompt, plain_content, image_links, api_key)
                        if not final_template.startswith("Error:"):
                            st.session_state.final_template = final_template
                            st.session_state.template_source = "AI Generated"
                            st.success("✅ AI template generated!")
                        else:
                            st.error(f"AI Generation failed: {final_template}")

    with col2:
        st.subheader("📄 Final Email Template")

        if hasattr(st.session_state, 'final_template'):
            st.success(f"✅ {st.session_state.template_source}")

            # Template actions
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download HTML",
                    st.session_state.final_template,
                    file_name="email_template.html",
                    mime="text/html",
                    use_container_width=True,
                    key="download_final"
                )
            with col2:
                if st.button("🔄 New Template", use_container_width=True, key="new_template"):
                    if 'final_template' in st.session_state:
                        del st.session_state.final_template
                    st.rerun()
            with col3:
                if st.button("📋 Copy Code", use_container_width=True, key="copy_code"):
                    st.code(st.session_state.final_template, language='html')

            # Display options
            tab1, tab2 = st.tabs(["📝 HTML Code", "👀 Live Preview"])

            with tab1:
                st.code(st.session_state.final_template, language='html')

            with tab2:
                st.components.v1.html(st.session_state.final_template, height=600, scrolling=True)

        else:
            st.info("👆 Configure your template and content, then generate to see the result")

            # Template showcase
            with st.expander("🎨 Available Templates"):
                template_cols = st.columns(2)
                templates_list = list(EMAIL_TEMPLATES.keys())

                for i, template_name in enumerate(templates_list):
                    with template_cols[i % 2]:
                        st.write(f"**{template_name}**")
                        # Show a small preview of the template
                        if st.button(f"Select {template_name}", key=f"select_{i}"):
                            st.session_state.preset_selected = template_name
                            st.rerun()


if __name__ == "__main__":
    main()