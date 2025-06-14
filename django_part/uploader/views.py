from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import UploadedImage
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
import json

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring Gemini: {str(e)}")
    raise

# Create your views here.

class LandingView(TemplateView):
    template_name = 'uploader/landing.html'

class AboutView(TemplateView):
    template_name = 'uploader/about.html'

class ContactView(TemplateView):
    template_name = 'uploader/contact.html'

class ChatbotView(TemplateView):
    template_name = 'uploader/chatbot.html'

class ExtractorView(TemplateView):
    template_name = 'uploader/upload.html'

    def post(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            print(f"Received image: {image_file.name}, type: {image_file.content_type}, size: {image_file.size} bytes")
            
            # Save the image
            uploaded_image = UploadedImage.objects.create(image=image_file)
            print(f"Image saved to: {uploaded_image.image.path}")
            
            try:
                # Get the processed image data from JavaScript
                processed_image_data = json.loads(request.POST.get('processed_image', '{}'))
                if not processed_image_data:
                    return JsonResponse({'success': False, 'message': 'No processed image data provided'})

                # Extract base64 data from the processed image
                base64_data = processed_image_data['data'].split(',')[1]
                image_bytes = base64.b64decode(base64_data)

                # Create image part for Gemini
                image_part = {
                    "mime_type": processed_image_data['mime_type'],
                    "data": image_bytes
                }
                print(f"Prepared image part with mime_type: {image_part['mime_type']}")
                
                # Generate content with the image
                print("Sending to Gemini...")
                prompt = """
                Extract and list ONLY the following information from this document:
                1. Document Type (e.g., Citizenship, Passport, License)
                2. Document Number/ID
                3. Full Name
                4. Date of Birth
                5. Address
                6. Issue Date
                7. Expiry Date (if any)
                8. Any other important numbers or codes

                Format the response as a simple list with clear labels.
                If any information is not found, write "Not found" for that item.
                Do not include any analysis or additional text.
                """
                
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
                return JsonResponse({
                    'success': False,
                    'message': f'Error processing image: {str(e)}'
                }, status=500)
                
        return self.get(request, *args, **kwargs)

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
