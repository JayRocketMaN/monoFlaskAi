# import os
# from dotenv import load_dotenv
# from itsdangerous import URLSafeTimedSerializer
# from flask import redirect, flash, url_for
# import brevo
# #from brevo import ApiException
# from brevo.core.api_error import ApiError
# #from brevo.transactional_emails import SendTransacEmailRequestSender, SendTransacEmailRequestToItem

# load_dotenv()
# client = brevo.Configuration()
# client.api_key['api-key'] = os.environ.get("BREVO_API_KEY")
# serializer = URLSafeTimedSerializer(os.environ.get("SECRET-KEY"))

# def brevo_reset_email(user_email, reset_url):
#     api_key = os.environ.get('BREVO_API_KEY')
#     api_instance = brevo.transactional_emailsApi(
#     brevo.ApiClient(client)
#     )
#     send_smtp_email = brevo.SendSmtpEmail(
#             to=[{"email":user_email}],
#             sender={"name": "monoFlask AI", "email": "odidikaanthony02@gmail.com"},
#             subject="Reset Your Password",
#             html_content=f"""
#                 <h3>Hello,</h3>
#                 <p>You requested a password reset. Click the link below to reset it:</p>
#                 <p><a href="{reset_url}">Reset My Password</a></p>
#                 <p>If you did not request this, please ignore this email.</p>
#                 <p>This link will expire in 15 minutes.</p>
#             """
#         )
#     try:
#         api_instance.send_transac_email(send_smtp_email)
#     except ApiError as e:
#         print(f"Brevo API Error: {e}")





















# # reset = os.getenv('RESET_PASSWORD')
# # def welcomeMail():
# #     form = RegisterationForm()
# #     email = form.email.data
# #     username = form.username.data
 
# #     EMAIL = 'odidikaanthony02@gmail.com'
# #     message = url_for
# #     brevo_key = os.environ.get("BREVO_API_KEY")
# #     if brevo_key:
# #                 print(f"DEBUG: I found the key! It starts with: {brevo_key[:7]}...", flush=True)
# #     else:
# #                 print("DEBUG: THE KEY IS MISSING! os.getenv returned None.", flush=True)

        
# #     api_url = "https://api.brevo.com/v3/smtp/email"
# #     headers = {
# #                 "accept": "application/json",
# #                 "api-key": brevo_key,
# #                 "content-type": "application/json"
# #             }
            
# #     payload = {
# #                 "sender": {"name": "MonoFlask AI", "email": EMAIL},
# #                 "to":[{"email": EMAIL, "name": 'me'}],
# #                 "replyTo": [{"email": email, "name": username}], # The visitor's email goes here!
# #                 "subject": f"New Contact from {username}",
# #                 "htmlContent": f"<p><strong>Name:</strong> {username}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong>{{ url_for('eset') }}</p>"
# #             }
        
# #     try:
# #                 # Send the API request
# #                     response = requests.post(api_url, json=payload, headers=headers)
                    
# #                     print(f"--- BREVO STATUS: {response.status_code} ---", flush=True)
# #                     print(f"--- BREVO RESPONSE: {response.text} ---", flush=True)
                    
# #                     if response.status_code in [200, 201]:
# #                         flash('Message sent successfully!', 'success')
# #                         return redirect(url_for('home') + '#contact')
# #                     else:
# #                         print(f"BREVO ERROR: {response.status_code} - {response.text}") 
# #                         flash('Email provider rejected the message.', 'error')                
# #                         return redirect(url_for('home') + '#contact')
                    
# #     except Exception as e:
# #                 print(f"--- PYTHON ERROR: {str(e)} ---", flush=True)
# #                 flash(f'Error: {str(e)}', 'error')
            
# #                 return redirect(url_for('home' + '#contact'))
    



# # 

      
# # client.transactional_emails.send_transac_email(
# #     html_content=f"""
# #             <h3>Hello,</h3>
# #             <p>You requested a password reset. Click the link below to reset it:</p>
# #             <p><a href="{reset_url}">Reset My Password</a></p>
# #             <p>If you did not request this, please ignore this email.</p>
# #             <p>This link will expire in 15 minutes.</p>
# #         """,
# #         sender=SendTransacEmailRequestSender(
# #         email= EMAIL,
# #         name="from MonoFlask AI",
# #     ),
# #     subject="Password Reset",
# #     to=[
# #         SendTransacEmailRequestToItem(
# #             email="email",
# #             username="username",
# #         )
# #     ],
# # )


# # try:
# #     client.transactional_emails.send_transac_email(...)
# # except ApiError as e:
# #     print(e.status_code)
# #     print(e.body)


# # def send_brevo_reset_email(user_email, reset_url):
# #     api_instance = Brevo.TransactionalEmailsApi(Brevo.ApiClient(client))
  
    
# #     api_key = os.getenv("BREVO_API_KEY") 
# #     url = "https://api.brevo.com/v3/smtp/email"
    
# #     headers = {
# #         "accept": "application/json",
# #         "api-key": api_key,
# #         "content-type": "application/json"
# #     }
    
# #     payload = {
# #         "sender": {"name": "AI Chat", "email": "noreply@yourdomain.com"},
# #         "to":[{"email": user_email}],
# #         "subject": "Password Reset Request",
# #         "htmlContent": f"""
# #             <h3>Hello,</h3>
# #             <p>You requested a password reset. Click the link below to reset it:</p>
# #             <p><a href="{reset_url}">Reset My Password</a></p>
# #             <p>If you did not request this, please ignore this email.</p>
# #             <p>This link will expire in 1 hour.</p>
# #         """
# #     }
    
# #     response = requests.post(url, json=payload, headers=headers)
# #     return response.status_code in [201, 200]



# # #     import sib_api_v3_sdk
# # # from brevo import ApiException

# # # configuration = Brevo.Configuration()
# # # configuration.api_key['api-key'] = os.environ.get("BREVO_API_KEY")

# # # api_instance = Brevo.TransactionalApi(
# # #     sib_api_v3_sdk.ApiClient(configuration)
# # # )
# # # create_contact = sib_api_v3_sdk.CreateContact(
# # #     email="contact@example.com"
# # # )

# # # try:
# # #     api_response = api_instance.create_contact(create_contact)
# # #     print(api_response)
# # # except ApiException as e:
# # #     print(f"Exception: {e}")

    




# # configuration = brevo_python.Configuration()
# # configuration.api_key['api-key'] = app.config['BREVO_API_KEY']

# # def send_brevo_email(recipient_email, reset_url):
# #     api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
    
# #     # Define the email content
# #     send_smtp_email = brevo_python.SendSmtpEmail(
# #         to=[{"email": recipient_email}],
# #         sender={"name": "Your App", "email": "noreply@yourdomain.com"},
# #         subject="Reset Your Password",
# #         html_content=f"""
# #             <p>You requested a password reset.</p>
# #             <p>Click the link below to set a new password (expires in 30 mins):</p>
# #             <a href="{reset_url}">{reset_url}</a>
# #         """
# #     )

# #     try:
# #         api_instance.send_transac_email(send_smtp_email)
# #     except ApiException as e:
# #         print(f"Exception when calling Brevo API: {e}")







