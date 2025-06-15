import warnings
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Disable CUDA
warnings.filterwarnings('ignore', category=UserWarning)

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import UploadedImage, RPAScript
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
import json
from .chatbot import chatbot  # Import the chatbot instance
import traceback
import pandas as pd
from PIL import Image
from django.utils import timezone
import subprocess
from django.contrib import messages

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Create your views here.

class LandingView(TemplateView):
    template_name = 'uploader/landing.html'

class AboutView(TemplateView):
    template_name = 'uploader/about.html'

class ContactView(TemplateView):
    template_name = 'uploader/contact.html'

class ChatbotView(TemplateView):
    template_name = 'uploader/chatbot.html'
    
    def post(self, request, *args, **kwargs):
        try:
            print("Received chatbot request")
            data = json.loads(request.body)
            question = data.get('question')
            
            print(f"Question received: {question}")
            
            if not question:
                return JsonResponse({'success': False, 'message': 'No question provided'})
            
            # Get response from the chatbot
            print("Getting answer from chatbot...")
            answer = chatbot.get_answer(question)
            print(f"Answer received: {answer}")
            
            if not answer:
                return JsonResponse({
                    'success': False,
                    'message': 'No response generated. Please try again.'
                })
            
            return JsonResponse({
                'success': True,
                'answer': answer
            })
            
        except Exception as e:
            print(f"Error in chatbot view: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)

class ExtractorView(TemplateView):
    template_name = 'uploader/extractor.html'

    def post(self, request, *args, **kwargs):
        try:
            print("Received POST request to ExtractorView")
            
            if 'file' not in request.FILES:
                print("No file in request.FILES")
                return JsonResponse({
                    'success': False,
                    'message': 'No file provided'
                })
                
            image_file = request.FILES['file']
            print(f"Received file: {image_file.name}, type: {image_file.content_type}, size: {image_file.size} bytes")
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if image_file.content_type not in allowed_types:
                print(f"Invalid file type: {image_file.content_type}")
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid file type. Please upload a JPG or PNG image.'
                })
            
            # Validate file size (5MB limit)
            if image_file.size > 5 * 1024 * 1024:
                print(f"File too large: {image_file.size} bytes")
                return JsonResponse({
                    'success': False,
                    'message': 'File size exceeds 5MB limit'
                })
            
            try:
                # Save the image
                uploaded_image = UploadedImage.objects.create(image=image_file)
                print(f"Image saved to: {uploaded_image.image.path}")
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'Error saving the image. Please try again.'
                })
            
            try:
                # Process with Gemini
                with open(uploaded_image.image.path, 'rb') as f:
                    image_bytes = f.read()
                
                # Create image part for Gemini
                image_part = {
                    "mime_type": image_file.content_type,
                    "data": image_bytes
                }
                
                # Generate content with the image
                print("Sending to Gemini...")
                prompt = """Extract and return ONLY the text content from this image.
Do not add any descriptions, labels, or extra formatting.
Do not add any headers or section titles.
Just return the exact text as it appears in the image."""
                
                response = model.generate_content([prompt, image_part])
                print("Received response from Gemini")
                
                # Store the analysis result
                uploaded_image.analysis_result = response.text
                uploaded_image.save()
                print("Saved analysis result")
                
                return JsonResponse({
                    'success': True,
                    'message': 'Image processed successfully',
                    'analysis': response.text
                })
                
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                print("Traceback:")
                traceback.print_exc()
                return JsonResponse({
                    'success': False,
                    'message': f'Error processing image: {str(e)}'
                }, status=500)
                
        except Exception as e:
            print(f"Unexpected error in ExtractorView: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred'
            }, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = UploadedImage.objects.all().order_by('-uploaded_at')
        return context

def upload_view(request):
    if request.method == 'POST':
        try:
            # Get the uploaded file
            image_file = request.FILES.get('image')
            if not image_file:
                return JsonResponse({'success': False, 'message': 'No image file provided'})

            # Get the processed image data from JavaScript
            processed_image_data = json.loads(request.POST.get('processed_image', '{}'))
            if not processed_image_data:
                return JsonResponse({'success': False, 'message': 'No processed image data provided'})

            # Save the original file
            image = UploadedImage(image=image_file)
            image.save()

            # Extract base64 data from the processed image
            base64_data = processed_image_data['data'].split(',')[1]
            image_bytes = base64.b64decode(base64_data)

            # Create image part for Gemini
            image_part = {
                "mime_type": processed_image_data['mime_type'],
                "data": image_bytes
            }

            # Generate content using Gemini
            response = model.generate_content([
                "Analyze this image and provide a detailed description of what you see. Focus on any text, numbers, or important visual elements.",
                image_part
            ])

            # Save the analysis result
            image.analysis_result = response.text
            image.save()

            return JsonResponse({
                'success': True,
                'message': 'Image uploaded and analyzed successfully',
                'analysis': response.text
            })

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            })

    # GET request - show the upload form
    images = UploadedImage.objects.all().order_by('-uploaded_at')
    return render(request, 'uploader/upload.html', {'images': images})

class RPAView(TemplateView):
    template_name = 'uploader/rpa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scripts'] = RPAScript.objects.all().order_by('-uploaded_at')
        return context

    def post(self, request, *args, **kwargs):
        try:
            if 'upload' in request.POST:
                # Handle script upload
                if 'script_file' not in request.FILES:
                    messages.error(request, 'No script file provided')
                    return redirect('rpa')

                script_file = request.FILES['script_file']
                data_file = request.FILES.get('data_file')  # Optional data file
                
                # Validate script file type
                if not script_file.name.endswith('.py'):
                    messages.error(request, 'Only Python (.py) files are allowed for scripts')
                    return redirect('rpa')

                # Validate data file type if provided
                if data_file:
                    allowed_extensions = ('.xlsx', '.csv', '.json', '.pdf')
                    if not data_file.name.lower().endswith(allowed_extensions):
                        messages.error(request, 'Only Excel (.xlsx), CSV (.csv), JSON (.json), or PDF (.pdf) files are allowed for data')
                        return redirect('rpa')

                # Create new RPAScript object
                script = RPAScript.objects.create(
                    name=request.POST.get('name', script_file.name),
                    description=request.POST.get('description', ''),
                    script_file=script_file,
                    data_file=data_file
                )
                messages.success(request, 'Script uploaded successfully')
                
            elif 'run' in request.POST:
                script_id = request.POST.get('script_id')
                if not script_id:
                    messages.error(request, 'No script selected')
                    return redirect('rpa')
                
                script = RPAScript.objects.get(id=script_id)
                
                try:
                    # Create virtual environment if it doesn't exist
                    if not os.path.exists('rpa_env'):
                        subprocess.run(['python', '-m', 'venv', 'rpa_env'], check=True)
                    
                    # Install required packages based on data file type
                    packages = ['selenium', 'pandas', 'openpyxl', 'webdriver-manager']
                    
                    if script.data_file:
                        file_ext = os.path.splitext(script.data_file.name)[1].lower()
                        if file_ext == '.pdf':
                            packages.extend(['PyPDF2', 'pdfplumber'])
                        elif file_ext == '.json':
                            packages.append('json5')  # More robust JSON parser
                    
                    subprocess.run([
                        'rpa_env/bin/pip', 'install', 
                        *packages
                    ], check=True)
                    
                    # Run the script
                    script.last_run = timezone.now()
                    script.save()
                    
                    # Set up environment variables for the script
                    env = os.environ.copy()
                    if script.data_file:
                        env['RPA_DATA_FILE'] = script.data_file.path
                        env['RPA_DATA_TYPE'] = os.path.splitext(script.data_file.name)[1][1:]  # Remove the dot
                    
                    result = subprocess.run([
                        'rpa_env/bin/python', 
                        script.script_file.path
                    ], capture_output=True, text=True, env=env)
                    
                    if result.returncode == 0:
                        messages.success(request, 'Script executed successfully\n' + result.stdout)
                    else:
                        messages.error(request, 'Script execution failed\n' + result.stderr)
                        
                except Exception as e:
                    messages.error(request, f'Error running script: {str(e)}')
                
            elif 'delete' in request.POST:
                script_id = request.POST.get('script_id')
                if script_id:
                    RPAScript.objects.filter(id=script_id).delete()
                    messages.success(request, 'Script deleted successfully')
                
            return redirect('rpa')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('rpa')
