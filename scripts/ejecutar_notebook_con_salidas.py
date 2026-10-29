import os
import sys
import io
import json
import base64
import contextlib
import ast
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BASE_DIR = r"C:\Users\oscar\.gemini\antigravity\scratch\ml_no_supervisado"
NOTEBOOK_PATH = os.path.join(BASE_DIR, "notebooks", "Machine_Learning_No_Supervisado_Clustering_PCA_SVD.ipynb")

def run_notebook_and_populate_outputs():
    with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
        nb = json.load(f)

    global_scope = {
        '__name__': '__main__',
        'display': lambda x: print(x.to_string() if hasattr(x, 'to_string') else str(x))
    }
    
    execution_counter = 1

    for cell_idx, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue

        raw_source = "".join(cell["source"])
        outputs = []

        # Hook into matplotlib to capture figures
        plt.close('all')

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        tree = ast.parse(raw_source)
        last_expr = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_expr = tree.body.pop() # Remove last expression to eval it separately

        code_to_exec = compile(tree, f"<cell_{cell_idx}>", "exec")

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                exec(code_to_exec, global_scope)
                
                eval_val = None
                if last_expr is not None:
                    expr_code = compile(ast.Expression(last_expr.value), f"<cell_{cell_idx}_expr>", "eval")
                    eval_val = eval(expr_code, global_scope)

            # Check stdout
            stdout_text = stdout_capture.getvalue()
            if stdout_text:
                outputs.append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in stdout_text.splitlines()]
                })

            # Check evaluated expression (like df.head() or df_metricas)
            if eval_val is not None:
                if isinstance(eval_val, (pd.DataFrame, pd.Series)):
                    html_rep = eval_val.to_html()
                    plain_rep = str(eval_val)
                    outputs.append({
                        "data": {
                            "text/html": [html_rep],
                            "text/plain": [plain_rep]
                        },
                        "execution_count": execution_counter,
                        "metadata": {},
                        "output_type": "execute_result"
                    })
                elif eval_val is not None and not isinstance(eval_val, (plt.Figure, plt.Axes)):
                    plain_rep = repr(eval_val)
                    outputs.append({
                        "data": {
                            "text/plain": [plain_rep]
                        },
                        "execution_count": execution_counter,
                        "metadata": {},
                        "output_type": "execute_result"
                    })

            # Check if any matplotlib figures were created
            fig_nums = plt.get_fignums()
            for fig_num in fig_nums:
                fig = plt.figure(fig_num)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=110)
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode('utf-8')
                outputs.append({
                    "data": {
                        "image/png": img_b64,
                        "text/plain": [f"<Figure size {fig.get_size_inches()[0]*110:.0f}x{fig.get_size_inches()[1]*110:.0f} with {len(fig.axes)} Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                })
                plt.close(fig)

        except Exception as e:
            print(f"Error en celda {cell_idx}: {e}")
            outputs.append({
                "ename": type(e).__name__,
                "evalue": str(e),
                "output_type": "error",
                "traceback": [f"{type(e).__name__}: {str(e)}"]
            })

        cell["outputs"] = outputs
        cell["execution_count"] = execution_counter
        execution_counter += 1

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    # Also copy to root notebook_ml_no_supervisado.ipynb for convenience
    root_nb_path = os.path.join(BASE_DIR, "notebook_ml_no_supervisado.ipynb")
    with open(root_nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print(f"[OK] Notebook ejecutado y guardado con todas sus salidas en: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    run_notebook_and_populate_outputs()
