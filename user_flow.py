import retentioneering
import streamlit as st
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


from datetime import datetime, timedelta
import pandas as pd

# load sample data

def make_event_query(date):
    query = """SELECT  timestamp, user_id, entity_type FROM `safalta-294406.sf_dataset.events_views` 
                    WHERE DATE(timestamp)='{}'
                    """.format(date)
    return query


@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    data = query_job.to_dataframe()
    return data


retentioneering.config.update({
    'user_col': 'user_id',
    'event_col': 'entity_type',
    'event_time_col': 'timestamp',
})

#user_id = st.text_input('Enter User ID', 'Enter User ID')
today = datetime.today()
tomorrow = today + timedelta(days=10)
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', tomorrow)
if start_date > end_date:
    st.error('Error: End date must fall after start date.')

start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")
events_views_query = make_event_query(start_date)
df = run_query(events_views_query)

short_df = df[df.entity_type.isin(['course', 'page', 'app-home', 'Safalta', 'blog'])]
data = short_df[['user_id', 'entity_type', 'timestamp']]

st.write(short_df)
retentioneering.config.update({
    'user_col': 'user_id',
    'event_col': 'entity_type',
    'event_time_col': 'timestamp',
})

data.rete.plot_graph(norm_type=None,
                     weight_col=None,
                     thresh=250)
plt.show()


html_string = "
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Graph Editor</title>
  <script src="https://code.jquery.com/jquery-3.4.1.js"></script>
  <script src="https://static.server.retentioneering.com/files/d3.v4.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <script src="https://static.server.retentioneering.com/viztools/draw-graph.min.js" type="text/javascript"></script>
  <style type="text/css">
      .download {
        display: flex;
        align-items: center;
      }

      .download__btn {
        margin-right: 16px;
      }

      .download__link {
        color: inherit !important;
      }


      .watermark {
        width: 100%;
      }
      .watermark h3 {
        width: 100%;
        text-align: center;
      }

      .svg-watermark {
        width: 100%;
        font-size: 80px;
        fill: #c2c2c2;
        opacity: 0.3;
        font-family: Arial;
      }

      html {
        font-size: 10px;
      }

      circle {
        fill: #ccc;
        stroke: #333;
        stroke-width: 1.5px;
      }

      .circle.source_node {
        fill: #f3f310;
      }

      .circle.nice_node {
        fill: green;
      }

      .circle.bad_node {
        fill: red;
      }

      .link {
        fill: none;
        stroke: #666;
        stroke-opacity: 0.7;
      }

      #nice_target {
        fill: green;
      }

      .link.nice_target {
        stroke: green;
      }

      #source {
        fill: yellow;
      }

      .link.source {
        stroke: #f3f310;
      }

      .link.positive {
        stroke: green;
      }

      .link.negative {
        stroke: red;
      }

      #source {
        fill: orange;
      }

      .link.source1 {
        stroke: orange;
      }

      #bad_target {
        fill: red;
      }

      .link.bad_target {
        stroke: red;
      }
      text {
        font: 12px sans-serif;
        pointer-events: none;
      }

      main li {
        display: inline;
      }
      .graphlist {
        list-style-type: none;

      }
      .graphloader {
        margin-top: 5%;
        margin-bottom: 5%;
      }
      .graphloader input {
        margin: auto;
      }

      h1 {
        text-align: center;
      }

      .bottom-checkbox {
        margin-right: 5%;
        display: inline;
      }

      .checkbox-class {
        margin-right: 3px;
      }

      .node-edit {
        position: relative;
        font-size: 12px;
        border: none;
        background-color: rgba(1,1,1,0);
      }

      .node-edit:focus {
        background-color: #ddd;
      }

      #option {
        margin-left: 5px;
      }

      #freakingGraph {
        border: solid 2px black;
        /*position: relative;*/
      }

      .container {
        margin: 0!important;
        padding-right: 0!important;
        max-width: 1200px!important;
      }
      .col-8 {
        padding: 0px 4px 0px 2px!important;
      }
      .col-4 {
        padding-right: 0px!important;
      }
      @media (max-width: 576px) {
        form label {
          font-size: 10px;
        }
      }


      @media (max-width: 768px) {
        form label {
          font-size: 0.8rem;
        }
      }


      @media (max-width: 992px) {
        form label {
          font-size: 1rem;
        }
      }

      @media (max-width: 1200px) {
        form label {
          font-size: 1rem;
        }
      }

      @media (min-width: 1201px) {
        form label {
          font-size: 1.4rem;
        }
      }

  </style>
</head>
<body>



  <main>

    <div class="container">

        <div class="row">
          <div class="watermark" style="z-index: 1010; background-color: #FFF; width: 100%">
            <h3>Retentioneering</h3>
          </div>
          <div class="col-8">

            <div id="freakingGraph" style="z-index: 1000">
              <!-- graph will be appended here -->
            </div>
          </div>
          <div class="col-4" style="z-index: 1010; background-color: #FFF">
            <form>
              <div id="check-boxes">

              </div>
              <br>
              <input name="submit" value="Update nodes" style="width: 80%;" type="button" onclick="changeNodes()">

            </form>

            <br>
            <br>
            <div style="z-index: 1010; background-color: #FFF">
              <h6>Nodes Threshold</h6>
              <input id="threshold-node-range" name="threshold-node" type="range" min="0" max="1" step="0.01" value="0.05"
              oninput="updateNodeThresholdText(this.value)" onchange="updateNodeThresholdText(this.value)">
              <label id="threshold-node-text">0.05</label>
            </div>
            <br>
            <div>
              <h6>Links Threshold</h6>
              <input id="threshold-link-range" name="threshold" type="range" min="0" max="1" step="0.01" value=0.002458718122719539
              oninput="updateLinkThresholdText(this.value*101679)" onchange="updateLinkThresholdText(this.value*101679)">
              <label id="threshold-link-text">0.002458718122719539</label>
            </div>
            <div>
              <input type="button" value="Set thresholds" onclick="setThresholds()">
            </div>
          </div>




          <div class="col-12" style="z-index: 1010; background-color: #FFF">

            <div class="weight-checkbox bottom-checkbox">
              <input type="checkbox" class="checkbox checkbox-class" checked value="weighted" id="show-weights"><label> Show weights </label>
            </div>

            <div class="percent-checkbox bottom-checkbox">
              <input type="checkbox" class="checkbox checkbox-class" checked id="show-percents"><label> Percents </label>
            </div>

            <div class="bottom-checkbox">
              <input type="checkbox" class="checkbox checkbox-class" checked id="show-names" onchange="changeNamesVisibility(this.checked)"><label> Show nodes names</label>
            </div>

            <div class="bottom-checkbox">
              <input type="checkbox" class="checkbox checkbox-class" id="block-targets" onchange="setLinkThreshold ()"><label> Show all edges for targets </label>
            </div>
            <div class="download">
              <div id="option" class="download__btn">
                <input name="downloadButton"
                type="button"
                value="download"
                onclick="downloadLayout()" />
              </div>
              <div class="download__btn">
                <button type="button" onclick="downloadSVG('svg', 'graph')">
                  download SVG
                </button>
              </div>
              <div class="download__btn">
                <button type="button" onclick="downloadPNG('svg', 'graph', 4)">
                  download PNG
                </button>
              </div>
            </div>
          </div>
      </div>




  </main>
  <script type="text/javascript">
    updateLinkThresholdText(0.002458718122719539*101679);
    initialize([{"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}], {}, [{"source": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "target": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "weight": 0.9744490012686986, "weight_text": 99081, "type": "suit"}, {"source": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "target": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "weight": 0.3361559417382154, "weight_text": 34180, "type": "suit"}, {"source": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "target": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "weight": 0.009982395578241328, "weight_text": 1015, "type": "suit"}, {"source": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "target": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "weight": 0.4258499788550241, "weight_text": 43300, "type": "suit"}, {"source": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "target": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "weight": 0.1007582686690467, "weight_text": 10245, "type": "suit"}, {"source": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "target": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "weight": 0.39699446296678764, "weight_text": 40366, "type": "suit"}, {"source": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "target": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "weight": 1.0, "weight_text": 101679, "type": "suit"}, {"source": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "target": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "weight": 0.006205804541744116, "weight_text": 631, "type": "suit"}, {"source": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "target": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "weight": 0.2211469428298862, "weight_text": 22486, "type": "suit"}, {"source": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "target": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "weight": 0.14908683208922197, "weight_text": 15159, "type": "suit"}, {"source": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "target": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "weight": 0.009992230450732206, "weight_text": 1016, "type": "suit"}, {"source": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "target": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "weight": 0.007494172838049155, "weight_text": 762, "type": "suit"}, {"source": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "target": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "weight": 0.35343581270468827, "weight_text": 35937, "type": "suit"}, {"source": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "target": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "weight": 0.04564364323016552, "weight_text": 4641, "type": "suit"}, {"source": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "target": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "weight": 0.027547477846949716, "weight_text": 2801, "type": "suit"}, {"source": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "target": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "weight": 0.3277766303759872, "weight_text": 33328, "type": "suit"}, {"source": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "target": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "weight": 0.29481997265905446, "weight_text": 29977, "type": "suit"}, {"source": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "target": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "weight": 0.051583906214655924, "weight_text": 5245, "type": "suit"}, {"source": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "target": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "weight": 0.4495421866855496, "weight_text": 45709, "type": "suit"}, {"source": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "target": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "weight": 0.4595442520087727, "weight_text": 46726, "type": "suit"}, {"source": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "target": {"index": 4, "name": "Safalta", "x": 75.0, "y": 108.9595178319209, "type": "suit_node", "degree": 33.85429775795711}, "weight": 0.1648718024370814, "weight_text": 16764, "type": "suit"}, {"source": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "target": {"index": 0, "name": "app-home", "x": 454.48777280324737, "y": 67.89297054025955, "type": "suit_node", "degree": 34.0}, "weight": 0.12086074804040166, "weight_text": 12289, "type": "suit"}, {"source": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "target": {"index": 3, "name": "blog", "x": 265.84965651203277, "y": 50.0, "type": "suit_node", "degree": 14.231229763577495}, "weight": 0.03253375819982494, "weight_text": 3308, "type": "suit"}, {"source": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "target": {"index": 2, "name": "course", "x": 458.0, "y": 283.0, "type": "suit_node", "degree": 31.388508766570958}, "weight": 0.4271875215137836, "weight_text": 43436, "type": "suit"}, {"source": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "target": {"index": 1, "name": "page", "x": 298.02590247925355, "y": 269.240479308097, "type": "suit_node", "degree": 31.366821430753255}, "weight": 0.8310368906067133, "weight_text": 84499, "type": "suit"}], 0);

    if (!1) {
      $('.percent-checkbox').hide();
    }
  </script>
</body>
</html>
"

st.markdown(html_string, unsafe_allow_html=True)
