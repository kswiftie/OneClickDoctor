from .start import router as start_router
from .navigation import router as navigation_router
from .search import router as search_router
from .select_doctor import router as select_doctor_router

__all__ = [
    'start_router',
    'navigation_router', 
    'search_router',
    'select_doctor_router'
]
