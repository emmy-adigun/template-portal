import requests
import streamlit as st
import time
import re

# Pre-defined HTML email templates
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
                        <td align="center" style="padding: 30px 20px; background-color: #2c3e50; color: #ffffff;">
                            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">[COMPANY_NAME]</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px;">[EMAIL_TITLE]</p>
                        </td>
                    </tr>
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #2c3e50; margin-top: 0;">[CONTENT_HEADING]</h2>
                            <p style="font-size: 16px; color: #333333; line-height: 1.6;">[MAIN_CONTENT]</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="[CTA_LINK]" style="background-color: #e74c3c; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">[CTA_TEXT]</a>
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
                        <td align="center" style="padding: 30px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff;">
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
                            <h2 style="color: #333333; margin-top: 0;">[CONTENT_HEADING]</h2>
                            <p style="font-size: 16px; color: #666666; line-height: 1.6;">[MAIN_CONTENT]</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="[SHOP_LINK]" style="background-color: #28a745; color: #ffffff; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; display: inline-block;">[CTA_BUTTON]</a>
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
                        <td align="center" style="padding: 30px 20px; background-color: #8b4513; color: #ffffff;">
                            <h1 style="margin: 0; font-size: 28px; font-family: 'Times New Roman', serif;">[NEWSLETTER_TITLE]</h1>
                            <p style="margin: 10px 0 0 0; font-size: 16px; font-style: italic;">[NEWSLETTER_DATE]</p>
                        </td>
                    </tr>
                    <!-- Featured Article -->
                    <tr>
                        <td style="padding: 30px;">
                            <h2 style="color: #8b4513; border-bottom: 2px solid #d4a574; padding-bottom: 10px;">[FEATURED_HEADING]</h2>
                            <p style="font-size: 16px; color: #333333; line-height: 1.8;">[FEATURED_CONTENT]</p>
                        </td>
                    </tr>
                    <!-- Secondary Content -->
                    <tr>
                        <td style="padding: 0 30px 30px 30px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td width="48%" style="padding: 15px; background-color: #f9f9f9; border: 1px solid #eeeeee;">
                                        <h3 style="color: #8b4513; margin-top: 0;">[SECTION1_HEADING]</h3>
                                        <p style="font-size: 14px; color: #666666;">[SECTION1_CONTENT]</p>
                                    </td>
                                    <td width="4%"></td>
                                    <td width="48%" style="padding: 15px; background-color: #f9f9f9; border: 1px solid #eeeeee;">
                                        <h3 style="color: #8b4513; margin-top: 0;">[SECTION2_HEADING]</h3>
                                        <p style="font-size: 14px; color: #666666;">[SECTION2_CONTENT]</p>
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
                            <h1 style="margin: 0; font-size: 24px; color: #333333; font-weight: 300;">[BRAND_NAME]</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 0; border-top: 1px solid #eeeeee; border-bottom: 1px solid #eeeeee;">
                            <h2 style="color: #333333; font-size: 20px; font-weight: 400; margin-top: 0;">[CONTENT_TITLE]</h2>
                            <p style="font-size: 16px; color: #666666; line-height: 1.6; margin-bottom: 30px;">[MAIN_CONTENT]</p>
                            <a href="[ACTION_LINK]" style="color: #007bff; text-decoration: none; font-size: 16px;">[ACTION_TEXT] →</a>
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


def replace_template_content(template, content_data):
    """
    Replace placeholder content in the template with user content
    """
    replaced_template = template

    for placeholder, content in content_data.items():
        if content:  # Only replace if content is provided
            replaced_template = replaced_template.replace(f"[{placeholder}]", content)

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


# Streamlit App
def main():
    st.set_page_config(
        page_title="📧 Smart Email Template Generator",
        page_icon="✉️",
        layout="wide"
    )

    st.title("📧 Smart Email Template Generator")
    st.markdown("**Choose a template OR generate custom templates with AI**")

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

            # Show template preview
            if selected_template:
                with st.expander("👀 Template Preview", expanded=True):
                    st.components.v1.html(EMAIL_TEMPLATES[selected_template], height=300, scrolling=True)

                st.success(f"✅ Selected: {selected_template}")

        else:  # AI Generation
            st.subheader("🤖 AI Template Generation")
            ai_prompt = st.text_input(
                "Describe the template you want:",
                placeholder="e.g., Modern corporate newsletter with blue theme"
            )

        st.subheader("📝 Your Content")

        # Content input based on template type
        if template_method == "📁 Use Pre-built Template" and selected_template:
            # Dynamic content fields based on template
            content_data = {}

            if selected_template == "Modern Corporate":
                content_data["COMPANY_NAME"] = st.text_input("Company Name", "Your Company")
                content_data["EMAIL_TITLE"] = st.text_input("Email Title", "Important Announcement")
                content_data["CONTENT_HEADING"] = st.text_input("Content Heading", "Latest Updates")
                content_data["MAIN_CONTENT"] = st.text_area("Main Content",
                                                            "Share your important news and updates here...", height=100)
                content_data["CTA_TEXT"] = st.text_input("Button Text", "Learn More")
                content_data["CTA_LINK"] = st.text_input("Button Link", "#")

            elif selected_template == "E-commerce Promotional":
                content_data["PROMOTION_TITLE"] = st.text_input("Promotion Title", "Special Offer!")
                content_data["PROMOTION_SUBTITLE"] = st.text_input("Promotion Subtitle", "Limited Time Only")
                content_data["HERO_IMAGE"] = st.text_input("Hero Image URL", "https://via.placeholder.com/560x200")
                content_data["CONTENT_HEADING"] = st.text_input("Content Heading", "Don't Miss Out!")
                content_data["MAIN_CONTENT"] = st.text_area("Main Content", "Describe your amazing offer here...",
                                                            height=100)
                content_data["CTA_BUTTON"] = st.text_input("Button Text", "Shop Now")
                content_data["SHOP_LINK"] = st.text_input("Shop Link", "#")
                content_data["UNSUBSCRIBE_LINK"] = st.text_input("Unsubscribe Link", "#")

            elif selected_template == "Newsletter":
                content_data["NEWSLETTER_TITLE"] = st.text_input("Newsletter Title", "Monthly Newsletter")
                content_data["NEWSLETTER_DATE"] = st.text_input("Date", "January 2024")
                content_data["FEATURED_HEADING"] = st.text_input("Featured Heading", "Featured Story")
                content_data["FEATURED_CONTENT"] = st.text_area("Featured Content", "Your main featured content...",
                                                                height=80)
                content_data["SECTION1_HEADING"] = st.text_input("Section 1 Heading", "Latest News")
                content_data["SECTION1_CONTENT"] = st.text_area("Section 1 Content", "First section content...",
                                                                height=60)
                content_data["SECTION2_HEADING"] = st.text_input("Section 2 Heading", "Upcoming Events")
                content_data["SECTION2_CONTENT"] = st.text_area("Section 2 Content", "Second section content...",
                                                                height=60)
                content_data["NEWSLETTER_FOOTER"] = st.text_input("Footer Text", "Thank you for reading!")

            elif selected_template == "Minimal Modern":
                content_data["BRAND_NAME"] = st.text_input("Brand Name", "Your Brand")
                content_data["CONTENT_TITLE"] = st.text_input("Content Title", "Important Update")
                content_data["MAIN_CONTENT"] = st.text_area("Main Content", "Your concise message here...", height=100)
                content_data["ACTION_TEXT"] = st.text_input("Action Text", "Learn more")
                content_data["ACTION_LINK"] = st.text_input("Action Link", "#")
                content_data["FOOTER_TEXT"] = st.text_input("Footer Text", "Sent with ❤️ from Your Brand")

            st.session_state.content_data = content_data

        else:  # AI Generation content
            content_text = st.text_area(
                "Enter your email content:",
                height=120,
                placeholder="Paste or type the content you want in the email..."
            )

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
            button_label = "🪄 Apply Content to Template"
        else:
            button_label = "🤖 Generate AI Template"

        if st.button(button_label, type="primary", use_container_width=True):
            if template_method == "📁 Use Pre-built Template":
                if selected_template:
                    # Replace content in selected template
                    template = EMAIL_TEMPLATES[selected_template]
                    final_template = replace_template_content(template, st.session_state.content_data)
                    st.session_state.final_template = final_template
                    st.session_state.template_source = f"Pre-built: {selected_template}"
                    st.success("✅ Content applied to template!")
                else:
                    st.error("Please select a template")

            else:  # AI Generation
                if not api_key:
                    st.error("🔑 API key required for AI generation")
                elif not ai_prompt.strip():
                    st.error("💬 Please describe the template you want")
                else:
                    with st.spinner("🤖 Generating your custom template..."):
                        final_template = quick_email_template(ai_prompt, content_text, image_links, api_key)
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
                    use_container_width=True
                )
            with col2:
                if st.button("🔄 New Template", use_container_width=True):
                    if 'final_template' in st.session_state:
                        del st.session_state.final_template
                    st.rerun()
            with col3:
                if st.button("📋 Copy Code", use_container_width=True):
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
                        st.caption(EMAIL_TEMPLATES[template_name][:100] + "...")
                        if st.button(f"Select {template_name}", key=f"select_{i}"):
                            st.session_state.preset_selected = template_name
                            st.rerun()


if __name__ == "__main__":
    main()