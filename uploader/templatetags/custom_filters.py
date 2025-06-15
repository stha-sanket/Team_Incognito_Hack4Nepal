from django import template

register = template.Library()

@register.filter
def split_lines(text):
    """Split text into lines and remove empty lines"""
    if not text:
        return []
    return [line for line in text.split('\n') if line.strip()]

@register.filter
def is_heading(text):
    """Check if the line is a heading (all uppercase)"""
    return text.strip().upper() == text.strip()

@register.filter
def starts_with(text, char):
    """Check if text starts with a specific character"""
    return text.strip().startswith(char) 