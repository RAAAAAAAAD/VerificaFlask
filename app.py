from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the data
dati_clienti = pd.read_csv('/workspace/VerificaFlask/data/dati_clienti.csv')

@app.route('/')
def homepage():
    risultato = sorted(list(set(dati_clienti['Country'])))
    return render_template('index.html', lista=risultato)

@app.route('/elencocitta/<nazione>', methods=['GET'])
def citta(nazione):
    info = dati_clienti[dati_clienti['Country'] == nazione]
    city_counts = info['City'].value_counts().sort_values(ascending=False)
    return render_template('radiobutton.html', tabella=city_counts)

@app.route('/elencoclienti', methods=['GET'])
def clienti():
    citta = request.args.get('citta')
    info = dati_clienti[dati_clienti['City'] == citta]
    return render_template('clienti.html', tabella=info.to_html())

@app.route('/elimina_cliente', methods=['GET', 'POST'])
def elimina_cliente():
    global dati_clienti
    msg = ''
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        if customer_id in dati_clienti['CustomerID'].values:
            dati_clienti = dati_clienti[dati_clienti['CustomerID'] != customer_id]
            dati_clienti.to_csv('/workspace/VerificaFlask/data/dati_clienti.csv', index=False)
            msg = 'Cliente eliminato.'
        else:
            msg = 'Cliente inesistente.'
    
    return render_template('elimina_cliente.html', msg=msg) 

@app.route('/aggiungi_cliente', methods=['GET', 'POST'])
def aggiungi_cliente():
    global dati_clienti
    msg = ''
    if request.method == 'POST':
        new_row = {
            'CustomerID': int(request.form['customer_id']),
            'CustomerName': request.form['customer_name'],
            'ContactName': request.form['contact_name'],
            'Address': request.form['address'],
            'City': request.form['city'],
            'PostalCode': request.form['postal_code'],
            'Country': request.form['country']
        }
        new_df = pd.DataFrame([new_row])
        dati_clienti = pd.concat([dati_clienti, new_df], ignore_index=True)
        dati_clienti.to_csv('/workspace/VerificaFlask/data/dati_clienti.csv', index=False)
        msg = 'Cliente aggiunto con successo!'
    
    return render_template('aggiungi_cliente.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32457, debug=True)
