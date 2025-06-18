import json
import time
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .unified_service import process_tds_question

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST", "GET"])
def virtual_ta_api(request):
    """TDS Virtual TA API endpoint"""
    start_time = time.time()
    
    try:
        # Parse request
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        image_b64 = data.get('image', '')
        
        if not question:
            return JsonResponse({
                'answer': 'Please provide a question for the TDS Virtual TA.',
                'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Course Forum'}]
            }, status=400)
        
        # Process with unified service
        response = process_tds_question(question, image_b64)
        
        # Ensure response within 30 seconds
        elapsed = time.time() - start_time
        if elapsed > 28:
            logger.warning(f"Response took {elapsed:.2f} seconds")
        
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
        
    except json.JSONDecodeError:
        return JsonResponse({
            'answer': 'Invalid JSON format in request.',
            'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Course Forum'}]
        }, status=400)
    except Exception as e:
        logger.error(f"API error: {e}")
        return JsonResponse({
            'answer': 'An error occurred processing your question. Please try again.',
            'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Course Forum'}]
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'TDS Virtual TA',
        'version': '1.0.0'
    })
