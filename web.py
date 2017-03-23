
#primera parte montar servidor
import http.server
import http.client
import json
import socketserver

'search=patient.drugs.medicinalproduct:"LYRICA"'+'&limit=10'

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    LIMIT = '&limit=10'
    RECEIVE_LIMIT="?limit=10"

    # GET, metodo GET
    def do_GET(self): #en self controlamos la orden
        self.do_head()
        # Send message back to client
        html = self.main_page()
        # Write content as utf-8 data
        self.send_ans(html)
        return

    def do_head(self):
        # Send response status code
        self.send_response(200)#respuesta de que todo va bien, el self es el handler
        # Send headers
        self.send_header("Content-type","text/html") #va a devolver contenidos en http
        self.end_headers()
        return

    def main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA ingenieros chulos</title>
            </head>
            <body>
            <h1>OPEN FDA client</>
                <form method="get" action="receive">
                    <input type="submit" value="listDrugs">
                    </input>
                </form>
                <form method="get" action="search">
                    </input>
                    <input type="submit" value="Drug search LYRICA">
                    </input>
                    </form>
                <form method="get" action="search">
                    medicamento: <input type="text" name="Drug"></input>
                    <input type="submit" value="Search companynumb"></input>
                    </form>
                <form method="get" action="search">
                    companynumb: <input type="text" name="companynumb"></input>
                    <input type="submit" value="Search medical product"></input>
                    </form>
            </body>
        </html>
        '''

        return html

#-------------- get_events

    def get_events(self,item,query):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        if item or query =='':
            connection.request("GET",self.OPENFDA_API_EVENT + self.RECEIVE_LIMIT)
        else:
            connection.request("GET",self.OPENFDA_API_EVENT+ query + item + self.LIMIT)
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

#----------parsing
    def get_list(self,event):
        drug=[]
        event1 = json.loads(event)
        results = event1["results"]
        for i in results:
            drug+= [i["patient"]["drug"][0]["medicinalproduct"]]
        return drug

    def get_companies_list(self,event):
        company=[]
        event1 = json.loads(event)
        results = event1["results"]
        for comp in results:
            company += [comp["companynumb"]]

        return company

#----------------------send_ANS

    def send_ans(self,html):
        if self.path == '/':
            return self.wfile.write(bytes(html, "utf8"))
        elif self.path=='/receive?':
            event=self.get_events('','')
            list_drugs=self.get_list(event)
            html=self.html_event(list_drugs)
        elif self.path == '/search?':
            drug = 'LYRICA'
            query = '?search=patient.drug.medicinalproduct:'
            event =self.get_events(drug,query)
            list_companies=self.get_companies_list(event)
            html= self.html_event(list_companies)
        elif '/search?Drug' in self.path:
            drug = self.path.split("=")[1]
            query = '?search=patient.drug.medicinalproduct:'
            event = self.get_events(drug,query)
            list_companies=self.get_companies_list(event)
            html=self.html_event(list_companies)
        elif '/search?companynumb' in self.path:
            number = self.path.split("=")[1]
            query = '?search=companynumb:'
            event = self.get_events(number,query)
            list_numbers=self.get_list(event)
            html = self.html_event(list_numbers)
        else:
            return self.wfile.write(bytes('Nanay',"utf8"))

        return self.wfile.write(bytes(html, "utf8"))

#---------------feed_HTML

    def html_event(self,items_list):
        s=''
        for item in items_list:
            s += "<li>"+item+"</li>"
        html='''
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        </html>''' %(s)
        return html
