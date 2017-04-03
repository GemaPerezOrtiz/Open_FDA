
#primera parte montar servidor
import http.server
import http.client
import json
import socketserver

#'search=patient.drugs.medicinalproduct:"LYRICA"'+'&limit=10'

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    LIMIT = '&limit='
    RECEIVE_LIMIT="?limit="

    # GET, metodo GET
    def do_GET(self):

        #self.send_response(200)#respuesta de que todo va bien, el self es el handler
        # Send message back to client
        html=self.send_ans()
        # Write content as utf-8 data
        if  html !='':
            self.send_response(200)
        else:
            self.send_response(404)
            html=self.html_not_found()

        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(bytes(html,"utf8"))
        #self.end_headers()
        return


    def main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA ingenieros chulos</title>
            </head>
            <body>
            <h1>OPEN FDA client</>
                <form method="get" action="listDrugs">
                    <input type="submit" value="listDrugs"></input>-----limit:<input type="text" name="limit"></input>
                </form>
                <form method="get" action="listCompanies">
                    <input type="submit" value="listCompanies LYRICA"></input>-----limit:<input type="text" name="limit"></input>

                    </form>
                <form method="get" action="searchDrug">
                    medicamento: <input type="text" name="drug"></input>
                    <input type="submit" value="searchDrug"></input>
                    </form>
                <form method="get" action="searchCompany">
                    company number: <input type="text" name="company"></input>
                    <input type="submit" value="searchCompany"></input>
                    </form>

                <form method="get" action="searchGender">
                    <input type="submit" value="listGenders"></input>-----limit:<input type="text" name="limit"></input>
                </form>
            </body>
        </html>
        '''

        return html

#-------------- get_events

    def get_events(self,item,query,limit):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        if item == query:
            connection.request("GET",self.OPENFDA_API_EVENT + self.RECEIVE_LIMIT+limit)
        else:
            connection.request("GET",self.OPENFDA_API_EVENT+ query + item + self.LIMIT+limit)
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

#----------parsing
    def get_list(self,event):
        drugs=[]
        event1 = json.loads(event)
        results = event1['results']
        for drug in results:
            drugs+= [drug["patient"]["drug"][0]["medicinalproduct"]]
        return drugs

    def get_companies_list(self,event):
        companies=[]
        event1 = json.loads(event)
        results = event1['results']
        for company in results:
            companies += [company["companynumb"]]

        return companies

    def get_genders_list(self,event):
        genders=[]
        event1 = json.loads(event)
        results = event1['results']
        for gender in results:
            genders += [gender["patient"]["patientsex"]]

        return genders

#----------------------send_ANS

    def send_ans(self):
        html=''
        if self.path == '/':
            html=self.main_page()
        elif self.path.startswith('/listDrugs'):
            limit = self.path.split("=")[1]
            event=self.get_events('','',limit)
            list_drugs=self.get_list(event)
            html=self.html_event(list_drugs)

        elif self.path.startswith('/listCompanies'):
            drug = 'LYRICA'
            query = '?search=patient.drug.medicinalproduct:'
            limit = self.path.split("=")[1]
            event =self.get_events(drug,query,limit)
            list_companies=self.get_companies_list(event)
            html= self.html_event(list_companies)

        elif self.path.startswith('/searchDrug'):
            drug = self.path.split("=")[1]
            query = '?search=patient.drug.medicinalproduct:'
            event = self.get_events(drug,query,'35')
            if drug in event:
                list_companies=self.get_companies_list(event)
                html=self.html_event(list_companies)
            else:
                html=''

        elif self.path.startswith('/searchCompany'):
            number = self.path.split("=")[1]
            print(number)
            query = "?search=companynumb:"
            event = self.get_events(number,query,'35')
            if number in event:
                list_numbers=self.get_list(event)
                html = self.html_event(list_numbers)
            else:
                html=''

        elif self.path.startswith('/searchGender'):
            limit = self.path.split("=")[1]
            event = self.get_events('','',limit)
            list_genders = self.get_genders_list(event)
            html = self.html_event(list_genders)
        #else:
            #html=''

        return html

#---------------feed_HTML

    def html_event(self,items_list):
        s=''
        for item in items_list:
            s += "<li>"+item+"</li>"
        html='''
        <html>
            <head></head>
                <body>
                    <ol>
                        %s
                    </ol>
                </body>
        </html>''' %(s)
        return html

    def html_not_found(self):
        html='''
        <html>
            <head>Error</head>
                <title>Error 404: not found</title>
            <body></body>
        </html>'''
        return html
