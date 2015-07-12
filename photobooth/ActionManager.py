from Action import Action

class ActionManager:
    def __init__(self):
        self.process_list = []

    def update_actions(self, elapsed):
        for process in self.process_list:
            if process.get_state() == Action.STATE_UNINITIALIZED:
                process.on_init()

            if process.get_state() == Action.STATE_RUNNING:
                process.on_update(elapsed)

            if process.is_dead():
                if process.get_state() == Action.STATE_SUCCEEDED:
                    process.on_succeed()

                    if process.has_child():
                        self.attach_action(process.get_child())

                elif process.get_state() == Action.STATE_FAILED:
                    process.on_fail()
                elif process.get_state() == Action.STATE_ABORTED:
                    process.on_abort()

                self.process_list.remove(process)

    def attach_action(self, process):
        self.process_list.append(process)

    def get_process_count(self):
        return len(self.process_list)

