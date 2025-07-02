import gradio as gr
from deals import Opportunity
from Agentic_Framework import Agentic_Framework 
import os

PORT = int(os.environ.get("PORT", 7860))
class App:
    def __init__(self):
        self.agentic_framework = None

    def run(self):
        with gr.Blocks(title = "Deals Finder",fill_width=True) as ui:
        
            def table_for(opps):
                # return [[opp.deal.product_description,f"{opp.deal.price:.2f}",f"{opp.estimate:.2f}",f"{opp.discount:.2f}",opp.deal.url] for opp in opps]
                return [[opp.deal.product_description, f"${opp.deal.price:.2f}", f"${opp.estimate:.2f}", f"${opp.discount:.2f}", opp.deal.url] for opp in opps]
            
            def start():
                self.agentic_framework = Agentic_Framework()
                opportunities = self.agentic_framework.memory
                table = table_for(opportunities)
                return table

            def update():
                self.agentic_framework.run()
                print("Update Function Ran")
                new_opportunities = self.agentic_framework.memory
                table = table_for(new_opportunities)
                return table

            def select_deal(selected_index:gr.SelectData):
                print(f"SELECTED INDEX: {selected_index.index} \n\n ")
                deal_index = selected_index.index[0]
                opportunities = self.agentic_framework.memory
                opportunity = opportunities[deal_index]
                self.agentic_framework.planner_agent.msg_agent.alert(opportunity)
            
            def test():
                print("Works")
                return "working"

            with gr.Row():
                gr.Markdown('<div style="text-align:center;font-size:20px">Deal Finder - An Autonomous Agentic Framework</div>')
            with gr.Row():
                opps_df = gr.Dataframe(
                    headers = ["Product Description","Price","Estimate","Discount","URL"],
                    row_count = 15,
                    wrap= True,
                    col_count = 5,
                    max_height = 1000,
                    column_widths = [7,1,1,1,2]
                )
            # with gr.Row():
            #    ts = gr.Textbox(label="Status",interactive=False)
            ui.load(start,inputs=[],outputs=[opps_df])
            timer = gr.Timer(value=60)
            timer.tick(update, inputs=[], outputs=[opps_df])
            # timer = gr.Timer(value = 60)
            # timer.tick(update,inputs=[],outputs=[opps_df])

            opps_df.select(select_deal)
        
        ui.launch(server_name="0.0.0.0",server_port = PORT)

if __name__ == "__main__":
    App().run()
