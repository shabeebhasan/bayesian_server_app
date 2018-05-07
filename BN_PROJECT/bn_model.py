from pomegranate import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def create_depression_model():

    sleep_disturbance = DiscreteDistribution({'true': 0.2, 'false': 0.8})
    fatigue = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.65],
            ['true', 'false', 0.35],
            ['false', 'true', 0.15],
            ['false', 'false', 0.85]
        ], [sleep_disturbance])
    dysthymia = ConditionalProbabilityTable(
        [
            ['true', 'true', 'true', 0.95],
            ['true', 'true', 'false', 0.05],
            ['true', 'false', 'true', 0.75],
            ['true', 'false', 'false', 0.25],
            ['false', 'true', 'true', 0.85],
            ['false', 'true', 'false', 0.15],
            ['false', 'false', 'true', 0.1],
            ['false', 'false', 'false', 0.9]
        ], [fatigue, sleep_disturbance])

    s1 = Node(sleep_disturbance, name="sleep_disturbance")
    s2 = Node(fatigue, name="fatigue")
    s3 = Node(dysthymia, name="dysthymia")

    model = BayesianNetwork("Depression Model")
    model.add_states(s1, s2, s3)
    model.add_edge(s1, s2)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.bake()
    return model

def predict_depression_rate(sleep_disturbance,fatigue):
    model = create_depression_model()
    result = model.predict_proba({'sleep_disturbance': sleep_disturbance, 'fatigue':fatigue})
    return '{0!s}%'.format(result[2].parameters[0]['true'] * 100)

cred = credentials.Certificate("/home/vagrant/app/bn_webapp/bn/fir_app_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://fir-app-404fc.firebaseio.com/'
})

users_list = []
users = db.reference('users').get()
for user in users:
    name = user
    parameters = users[user]
    fatigue = 'false'
    sleep_disturbance = 'false'
    for param in parameters:
        if parameters[param]['action'] == 'feeling':
            fatigue = 'false' if parameters[param]['reponse_type'] == 'positive' else 'true'
        elif parameters[param]['action'] == 'sleep_disturbance':
            sleep_disturbance = 'false' if parameters[param]['reponse_type'] == 'positive' else 'true'
    dp_rate = predict_depression_rate(sleep_disturbance, fatigue)
    users_list.append({'user_name': name, 'depression_rate': dp_rate})

print(users_list)

#print(predict_depression_rate(sleep_disturbance='false',fatigue='true'))
#model = create_depression_model()
#print(model.predict([['true', 'false', None],['true', 'false', None],[None, 'true', 'false']]))
#check user feel bad and sleep_full
#print(model.predict_proba({'sleep_disturbance': 'true', 'fatigue': 'true'}))
#print('DONE')
