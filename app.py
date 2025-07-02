import gradio as gr
from deals import Opportunity
from Agentic_Framework import Agentic_Framework 

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
            with gr.Row():
               ts = gr.Textbox(label="Status",interactive=False)
            ui.load(start,inputs=[],outputs=[opps_df])
            timer = gr.Timer(value=60)
            timer.tick(update, inputs=[], outputs=[opps_df])
            # timer = gr.Timer(value = 60)
            # timer.tick(update,inputs=[],outputs=[opps_df])

            opps_df.select(select_deal)
        
        ui.launch(share=False,inbrowser = True)

if __name__ == "__main__":
    App().run()

# import gradio as gr
# import threading
# import time
# from deals import Opportunity
# from Agentic_Framework import Agentic_Framework 

# class App:
#     def __init__(self):
#         self.agentic_framework = None
#         self.timer_running = False
#         self.timer_thread = None

#     def start_timer(self, interval=6):
#         """Start a background timer thread"""
#         if not self.timer_running:
#             self.timer_running = True
#             self.timer_thread = threading.Thread(target=self._timer_loop, args=(interval,))
#             self.timer_thread.daemon = True
#             self.timer_thread.start()

#     def stop_timer(self):
#         """Stop the background timer"""
#         self.timer_running = False
#         if self.timer_thread:
#             self.timer_thread.join()

#     def _timer_loop(self, interval):
#         """Background timer loop"""
#         while self.timer_running:
#             time.sleep(interval)
#             if self.timer_running:  # Check again in case it was stopped
#                 self.test()  # Call your test function
#                 # For the actual update, you'd need to trigger UI updates differently

#     def run(self):
#         with gr.Blocks(title="Deals Finder", fill_width=True) as ui:
        
#             def table_for(opps):
#                 return [[opp.deal.product_description, f"${opp.deal.price:.2f}", f"${opp.estimate:.2f}", f"${opp.discount:.2f}", opp.deal.url] for opp in opps]
            
#             def start():
#                 self.agentic_framework = Agentic_Framework()
#                 opportunities = self.agentic_framework.memory
#                 table = table_for(opportunities)
                
#                 # Start the timer when the app starts
#                 self.start_timer(6)
                
#                 return table

#             def update():
#                 if self.agentic_framework:
#                     self.agentic_framework.run()
#                     print("Update Function Ran")
#                     new_opportunities = self.agentic_framework.memory
#                     table = table_for(new_opportunities)
#                     return table
#                 return []

#             def select_deal(selected_index: gr.SelectData):
#                 print(f"SELECTED INDEX: {selected_index.index} \n\n ")
#                 deal_index = selected_index.index[0]
#                 opportunities = self.agentic_framework.memory
#                 opportunity = opportunities[deal_index]
#                 self.agentic_framework.planner_agent.msg_agent.alert(opportunity)
            
#             def test():
#                 print("Timer tick - Works!")
#                 return "Timer working"

#             # UI Components
#             with gr.Row():
#                 gr.Markdown('<div style="text-align:center;font-size:20px">Deal Finder - An Autonomous Agentic Framework</div>')
            
#             with gr.Row():
#                 opps_df = gr.Dataframe(
#                     headers=["Product Description", "Price", "Estimate", "Discount", "URL"],
#                     row_count=15,
#                     wrap=True,
#                     col_count=5,
#                     max_height=1000,
#                     column_widths=[7, 1, 1, 1, 2]
#                 )

#             # Manual update button for testing
#             with gr.Row():
#                 update_btn = gr.Button("Manual Update")
#                 test_btn = gr.Button("Test Function")
#                 timer_status = gr.Textbox(label="Timer Status", interactive=False)

#             # Event handlers
#             ui.load(start, inputs=[], outputs=[opps_df])
#             update_btn.click(update, inputs=[], outputs=[opps_df])
#             test_btn.click(test, inputs=[], outputs=[timer_status])
#             opps_df.select(select_deal)

#             # Try the original timer approach as backup
#             try:
#                 timer = gr.Timer(value=6, active=True)
#                 timer.tick(test, inputs=[], outputs=[timer_status])
#                 print("Gradio Timer initialized successfully")
#             except Exception as e:
#                 print(f"Gradio Timer failed to initialize: {e}")
        
#         # Enable queuing and launch
#         ui.queue()
#         ui.launch(share=False, inbrowser=True)

#         # Clean up timer when app closes
#         self.stop_timer()

# if __name__ == "__main__":
#     App().run()