#MIT License

#Copyright (c) [2017] [GEMA PEREZ ORTIZ]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#primera parte montar servidor
import http.server
import http.client
import json
import socketserver

'search=patient.drugs.medicinalproduct:"LYRICA"'+'&limit=10'

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    def get_companies(self,DRUG):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT +'?search=patient.drug.medicinalproduct:'+DRUG+'&limit=50')
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def get_medical_product(self,companumero): #sacar el evento bien!!!!!!!!!!!!****
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT +'?search=companynumb:'+companumero+'&limit=50')
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def get_event(self):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT + "?limit=10")
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA ingenieros chulos</title>
            </head>
            <body>
            <h1>OPEN FDA client</>
            <form method="get" action="receive">
                    <input type="submit" value="Druglist:Send to OpenFDA">
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

    def find_path(self):
        return print(self.path)

    def do_head(self):
        # Send response status code
        self.send_response(200)#respuesta de que todo va bien, el self es el handler
        # Send headers
        self.send_header("Content-type","text/html") #va a devolver contenidos en http
        self.end_headers()

        return

    def get_from_NUMBY_med(self,NUMB):
        meds=[]
        event = self.get_medical_product(NUMB)
        event1 = json.loads(event)
        results = event1["results"]
        for comp in results:
            meds += [comp["patient"]["drug"][0]["medicinalproduct"]]
        return meds

    def send_ans(self,html):
        if self.path == '/':
            return self.wfile.write(bytes(html, "utf8")) #fichero de escritura que llega al cliente
        elif self.path=='/receive?':
            #drug = self.get_DRUGS()
            html_ev = self.event_html_druglist()
            #results = event1['results']
            #html_ev = self.event_html(event)
            return self.wfile.write(bytes(html_ev, "utf8")) #estamos mandando al cliente el evento
        elif self.path == '/search?':
            html_compy = self.event_html_comp()
            return self.wfile.write(bytes(html_compy, "utf8"))
        elif '/search?Drug' in self.path:
            DRUG = self.path.split("=")[1]
            drug_ncompany=self.get_COMPY(DRUG)
            #drug_compy=self.get_COMPY(drug_company)
            html_vary=self.event_html_DRUG_variable(drug_ncompany)
            return self.wfile.write(bytes(html_vary, "utf8"))
        elif '/search?companynumb' in self.path:
            NUMB = self.path.split("=")[1]
            medic=self.get_medical_product(NUMB)
            numberdrug = self.get_from_NUMBY_med(NUMB)
            html_med = self.event_html_med(numberdrug)
            return self.wfile.write(bytes(html_med, "utf8"))
        else:
            return self.wfile.write(bytes('Nanay',"utf8"))



    # GET, metodo GET
    def do_GET(self): #en self controlamos la orden
        self.do_head()
        # Send message back to client
        html = self.main_page()
        # Write content as utf-8 data
        self.send_ans(html)
        return


    def get_DRUGS(self):
        drug=[]
        event = self.get_event()
        event1 = json.loads(event)
        results = event1['results']
        for i in results:
            drug+= [i["patient"]["drug"][0]["medicinalproduct"]]
        return drug

    def get_COMPY(self,DRUG):
        company=[]
        event = self.get_companies(DRUG)
        event1 = json.loads(event)
        results = event1["results"]
        for comp in results:
            company += [comp["companynumb"]]

        return company



    def event_html_druglist(self):
        products=self.get_DRUGS()
        #meds =""
        drugs_html='''
    <html>
    <head></head>
    <body>
        <ul>
        '''
        for drug in products:
            drugs_html +=" <li>"+drug+ "</li>\n"
        drugs_html+='''

        </ul>
    </body>
    </html>
        '''
        return drugs_html

    def event_html_comp(self):
        companies = self.get_COMPY('LYRICA')
        #print(companies)
        comp_html ='''
        <html>
        <head></head>
        <body>
            <ul>
            '''
        for comp in companies:
            comp_html += "<li>"+comp+ "</li>\n"
        comp_html+='''
            </ul>
        </body>
        </html>
        '''
        return comp_html

    def event_html_DRUG_variable(self,drug_company):
        variable_html='''
        <html>
        <head></head>
        <body>
            <ul>'''
        for event in drug_company:
            variable_html += "<li>"+event+"</li>\n"
        variable_html+='''
            </ul>
        </body>
        </html>
        '''
        return variable_html
    def event_html_med(self,medlist):
        med_html='''
        <html>
        <head></head>
        <body>
            <ul>'''
        for event in medlist:
            med_html += "<li>"+event+"</li>\n"
        med_html+='''
            </ul>
        </body>
        </html>
        '''
        return med_html
