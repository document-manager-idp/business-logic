from enum import Enum
import hashlib
from unstructured.documents.elements import ElementType, Element, Table
class ElementCategory(Enum):
    TEXTUAL = "Textual"
    TABLE = "Table"
    IMAGE = "Image"
    OTHER = "Other"

def classify_element(element_type):
    categories = {
        ElementCategory.TEXTUAL: [
            ElementType.TITLE,
            ElementType.TEXT,
            ElementType.UNCATEGORIZED_TEXT,
            ElementType.NARRATIVE_TEXT,
            ElementType.BULLETED_TEXT,
            ElementType.PARAGRAPH,
            ElementType.ABSTRACT,
            ElementType.FIELD_NAME,
            ElementType.VALUE,
            ElementType.LINK,
            ElementType.COMPOSITE_ELEMENT,
            ElementType.FIGURE_CAPTION,
            ElementType.CAPTION,
            ElementType.LIST_ITEM,
            ElementType.LIST_ITEM_OTHER,
            ElementType.ADDRESS,
            ElementType.EMAIL_ADDRESS,
            ElementType.FORMULA,
            ElementType.HEADER,
            ElementType.HEADLINE,
            ElementType.SUB_HEADLINE,
            ElementType.PAGE_HEADER,
            ElementType.SECTION_HEADER,
            ElementType.PAGE_FOOTER,
        ],
        ElementCategory.IMAGE: [
            ElementType.IMAGE,
            ElementType.PICTURE,
        ],
        ElementCategory.TABLE: [
            ElementType.TABLE,
        ]
    }

    for category, options in categories.items():
        if element_type in options:
            return category
    
    return ElementCategory.OTHER

def get_hash(string: str) -> int:
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def get_id(url: str, chunk_number: int) -> str:
    hash = get_hash(url)
    return f'{hash}-{chunk_number}'

def get_table_id(table_markdown: str) -> str:
    return get_hash(table_markdown)
