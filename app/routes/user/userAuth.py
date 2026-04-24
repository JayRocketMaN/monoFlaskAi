from flask import request, jsonify, Blueprint, redirect, url_for, render_template
from flask_login import current_user
from flask_login import login_required
from app.launchGenai import generate 
from app.models.allModels import ChatSession, ChatMessage, Users
from datetime import datetime
import uuid

user_bp = Blueprint('user', __name__)


@user_bp.route('/response/<session_id>', methods=['POST'])
@user_bp.route('/response/', methods=['POST'])
@login_required
def AiResponse(session_id=None):
        #confirm request and current_session
        try:
            userInput = request.json.get('message', '').strip()
            if not userInput:
                return jsonify({'response': 'Empty message'}), 400
        
            if not current_user.all_conversations:
                new_id = str(uuid.uuid4())
                initial_session = ChatSession(
                session_id=new_id,
                title="First Conversation",
                messages=[]
                )
                current_user.update(push__all_conversations=initial_session)
                current_user.reload()
                session_id = new_id
            elif session_id is None:
                session_id = current_user.all_conversations[-1].session_id

            #generate AI Response
            try:
                final_response = generate(userInput)
                if not final_response:
                    raise ValueError("Gemini returned an empty response")
            except Exception as e:
                print(f"Gemini API Error: {e}")
                return jsonify({'response': 'The AI is temporarily unavailable. Please try again.'}), 503

            #create chat object to save
            user_msg = ChatMessage(sender='user', text=userInput)
            ai_msg = ChatMessage(sender='ai', text=final_response)

            #valiate and update chat session only
            session_count = Users.objects(
            id=current_user.id,
            all_conversations__session_id=session_id
            ).update(
            push_all__all_conversations__S__messages=[user_msg, ai_msg]
            )

            if session_count == 0:
               return jsonify({'response': 'Chat session not found.'}), 404
                    
            return jsonify({'response': final_response})
        except Exception as e:
              print(f"CRITICAL SYSTEM ERROR: {str(e)}")
        return jsonify({'response': 'A system error occurred. Please refresh the page.'}), 500


@user_bp.route('/new-chat')
@login_required
def new_chat():
    #Create a new unique session
    new_session = ChatSession(
        session_id=str(uuid.uuid4()),
        title=f"Chat {len(current_user.all_conversations) + 1}",
        messages=[]
    )    
    #Push to database
    current_user.update(push__all_conversations=new_session)
    
    return redirect(url_for('user.chat', session_id=new_session.session_id))

@user_bp.route('/')
@user_bp.route('/chat/<session_id>') 
@login_required
def chat(session_id=None): 
    all_sessions = current_user.all_conversations or []    
    active_session = None
    
    if all_sessions:
        if session_id:
            active_session = next((s for s in all_sessions if s.session_id == session_id), None)
            
            if not active_session:
                active_session = all_sessions[-1]
        else:
            active_session = all_sessions[-1] 

    return render_template('chat.html', 
                           active_session=active_session, 
                           all_sessions=all_sessions)


@user_bp.route('/delete-chat/<session_id>', methods=['POST'])
@login_required
def delete_chat(session_id):
    updated_count = Users.objects(id=current_user.id).update(
        pull__all_conversations__session_id=session_id
    )

    if updated_count == 0:
        return jsonify({'error': 'Chat not found'}), 404

    return redirect(url_for('user.chat'))


              
              






# import uuid
# from flask import request, jsonify
# from flask_login import login_required, current_user

# @user_bp.route('/response/<session_id>', methods=['POST'])
# @user_bp.route('/response/', methods=['POST'], defaults={'session_id': None})
# @login_required
# def AiResponse(session_id):
#     try:
#         # 1. Validate Input
#         data = request.get_json()
#         user_input = data.get('message', '').strip()
#         if not user_input:
#             return jsonify({'response': 'Please type a message first.'}), 400

#         # 2. Handle missing sessions (Auto-create)
#         if not current_user.all_conversations:
#             new_id = str(uuid.uuid4())
#             initial_session = ChatSession(
#                 session_id=new_id,
#                 title="First Conversation",
#                 messages=[]
#             )
#             current_user.update(push__all_conversations=initial_session)
#             current_user.reload()
#             session_id = new_id
#         elif session_id is None:
#             session_id = current_user.all_conversations[-1].session_id

#         # 3. Generate AI Response (with Gemini Error Handling)
#         try:
#             final_response = generate(user_input)
#             if not final_response:
#                 raise ValueError("Gemini returned an empty response")
#         except Exception as e:
#             print(f"Gemini API Error: {e}")
#             return jsonify({'response': 'The AI is temporarily unavailable. Please try again.'}), 503

#         # 4. Prepare Messages
#         user_msg = ChatMessage(sender='user', text=user_input)
#         ai_msg = ChatMessage(sender='ai', text=final_response)

#         # 5. Targeted Save (with validation that the session exists)
#         # We use 'updated_count' to check if the session_id was actually found
#         updated_count = Users.objects(
#             id=current_user.id,
#             all_conversations__session_id=session_id
#         ).update(
#             push_all__all_conversations__S__messages=[user_msg, ai_msg]
#         )

#         if updated_count == 0:
#             return jsonify({'response': 'Chat session not found.'}), 404

#         return jsonify({'response': final_response})

#     except Exception as e:
#         # Log the actual error to your terminal for debugging
#         print(f"CRITICAL SYSTEM ERROR: {str(e)}")
#         return jsonify({'response': 'A system error occurred. Please refresh the page.'}), 500

        
