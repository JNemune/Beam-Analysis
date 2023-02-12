import matplotlib.pyplot as plt
import re
import subprocess
import sys
# from information import w, v, m

class tex_plot(object):
    def __init__(self, w, v, m, sigma_max, tau_y_max, tau_xy_max, torque, ybar, ymax, Iyy, Izz) -> None:
        mathtext_demos = {
            "W(x)": rf'${w}$',
            "V(x)": rf'${v}$',
            "M(x)": rf'${m}$',
            "$\sigma_{max}(x)$": rf'${sigma_max}$',
            r"$\tau_{y,max}(x)$": rf'${tau_y_max}$',
            r"$\tau_{xy,max}(x)$": rf'${tau_xy_max}$',
            "T(x)": rf'${torque}$',
            "$y_{bar}$": rf'${ybar}$',
            "$y_{max}$": rf'${ymax}$',
            "$I_{yy}$": rf'${Iyy}$',
            "$I_{zz}$": rf'${Izz}$'
        }
        
        n_lines = len(mathtext_demos)


        def doall():
            # Colors used in Matplotlib online documentation.
            mpl_grey_rgb = (51 / 255, 51 / 255, 51 / 255)

            # Creating figure and axis.
            fig = plt.figure(figsize=(23,16))
            ax = fig.add_axes([0.01, 0.01, 0.98, 0.90],
                            facecolor="white", frameon=True)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            # ax.set_title("Matplotlib's math rendering engine",
            #              color=mpl_grey_rgb, fontsize=14, weight='bold')
            ax.set_xticks([])
            ax.set_yticks([])

            # Gap between lines in axes coords
            line_axesfrac = 1 / n_lines

            for i_line, (title, demo) in enumerate(mathtext_demos.items()):

                baseline = 1 - i_line * line_axesfrac
                baseline_next = baseline - line_axesfrac
                fill_color = ['white', 'tab:blue'][i_line % 2]
                ax.axhspan(baseline, baseline_next, color=fill_color, alpha=0.2)
                ax.annotate(rf'{title}:',
                            xy=(0.06, baseline - 0.3 * line_axesfrac),
                            color=mpl_grey_rgb, weight='bold', fontsize=22)
                ax.annotate(demo,
                            xy=(0.04, baseline - 0.75 * line_axesfrac),
                            color=mpl_grey_rgb, fontsize=18)

            plt.savefig('/var/www/html/static/latex.png')
            # plt.show()

        doall()
