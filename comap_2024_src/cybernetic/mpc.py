
class McpController:
    def __init__(self, model, cost, constraints, horizon, dt, mpc_dt, mpc_steps, mpc_mode, mpc_solver):
        self.model = model
        self.cost = cost
        self.constraints = constraints
        self.horizon = horizon
        self.dt = dt
        self.mpc_dt = mpc_dt
        self.mpc_steps = mpc_steps
        self.mpc_mode = mpc_mode
        self.mpc_solver = mpc_solver

    def solve(self, x0, u0, xref, uref, xlb, xub, ulb, uub):
        # ...
        return u


