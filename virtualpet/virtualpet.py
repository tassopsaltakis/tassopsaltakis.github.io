from flask import Flask, render_template, request, redirect, make_response
import json

app = Flask(__name__)

# Default pet stats
default_pet = {
    'name': 'Fluffy',
    'hunger': 50,
    'happiness': 50,
    'energy': 50
}

# Route to serve the virtual pet game
@app.route('/')
def home():
    # Try to get pet data from cookies
    pet_data = request.cookies.get('pet')

    if pet_data:
        pet = json.loads(pet_data)  # Load pet data from cookies
    else:
        pet = default_pet.copy()  # Use default stats if no cookies are found

    # Pass the pet data to the template
    return render_template('virtualpet.html', pet=pet)

# Route to update pet stats based on user interaction
@app.route('/interact', methods=['POST'])
def interact():
    action = request.form['action']

    # Load current pet stats from cookies
    pet_data = request.cookies.get('pet')
    pet = json.loads(pet_data) if pet_data else default_pet.copy()

    # Update pet stats based on user action
    if action == 'feed':
        pet['hunger'] = min(pet['hunger'] + 10, 100)
    elif action == 'play':
        pet['happiness'] = min(pet['happiness'] + 10, 100)
        pet['energy'] = max(pet['energy'] - 10, 0)
    elif action == 'sleep':
        pet['energy'] = min(pet['energy'] + 20, 100)

    # Save the updated pet stats back into cookies
    response = make_response(redirect('/'))
    response.set_cookie('pet', json.dumps(pet), max_age=30*24*60*60)  # Cookie lasts 30 days

    return response

if __name__ == '__main__':
    app.run(debug=True)
