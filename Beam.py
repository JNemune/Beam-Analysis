import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.abc import _clash1


class Beam(object):
    def __init__(
        self,
        lenght: float,
        F: float,
        W: float,
        FT: float,
        WT: float,
        xpin: float = 0.0,
        xroller: float | None = None,
    ) -> None:
        """
        Analysis of pin-roller and cantilever beams.

        Args:
            lenght, F, W, FT, FW are the geometric sections of the beam.

            If xroller is None, the beam is a cantilever, otherwise use xpin and xroller to specify pin and roller coordinates.
        """
        if xpin == xroller:
            raise Exception("xpin and xroller are the same!")
        self.__lenght = lenght
        self.__F = F
        self.__W = W
        self.__FT = FT
        self.__WT = WT
        self.__xpin = xpin
        self.__xroller = xroller

        self.__Area = W * WT + F * FT
        self.__C1W = 1 / 3 * (1 - 0.63 * W / WT)
        self.__C1F = 1 / 3 * (1 - 0.63 * F / FT)

        self.__ybar = (W / 2 * W * WT + W * F * FT) / self.__Area
        self.__ymax = -self.__ybar if self.__ybar > W / 2 else W - self.__ybar
        self.__Izz = (
            FT * F**3 / 12
            + F * FT * (W - self.__ybar) ** 2
            + W * WT**3 / 12
            + W * WT * (W / 2 - self.__ybar)
        )

        self.__Iyy = (
            F * FT**3 / 12
            + F * FT * (W - self.__ybar) ** 2
            + WT * W**3 / 12
            + W * WT * (W / 2 - self.__ybar)
        )

        self.__floads = []
        self.__mloads = []

        self.__x = symbols("x")

    def floading(self, x: str, y: str, x1: float, x2: float | None = None) -> None:
        """
        F = Fx(x) î + Fy(x) ĵ, [x1, x2]

        if x2 is None it is point loading.
        """
        if x2 is None:
            x2 = x1
        if x1 > x2:
            raise Exception("x1 <= x2")
        elif x2 > self.__lenght:
            raise Exception("x2 <= lenght")
        self.__floads.append(
            {
                "x": simplify(x, locals=_clash1),
                "y": simplify(y, locals=_clash1),
                "x1": x1,
                "x2": x2,
            }
        )

    def mloading(self, x: str, z: str, x1: float, x2: float | None = None) -> None:
        """
        M = Mx(x) î + Mz(x) k̂, [x1, x2]

        if x2 is None it is point loading.
        """
        if x2 is None:
            x2 = x1
        if x1 > x2:
            raise Exception("x1 <= x2")
        elif x2 > self.__lenght:
            raise Exception("x2 <= lenght")
        self.__mloads.append(
            {
                "x": simplify(x, locals=_clash1),
                "z": simplify(z, locals=_clash1),
                "x1": x1,
                "x2": x2,
            }
        )

    def __statical_analysis(self) -> None:
        # Solve for reactions
        self.__Nx = -sum(
            [
                i["x"]
                if i["x1"] == i["x2"]
                else integrate(i["x"], (self.__x, i["x1"], i["x2"]))
                for i in self.__floads
            ]
        )
        self.__Ny = -sum(
            [
                i["y"]
                if i["x1"] == i["x2"]
                else integrate(i["y"], (self.__x, i["x1"], i["x2"]))
                for i in self.__floads
            ]
        )
        self.__MzN = -sum(
            [
                (i["x1"] - self.__xpin) * i["y"]
                if i["x1"] == i["x2"]
                else integrate(
                    (self.__x - self.__xpin) * i["y"], (self.__x, i["x1"], i["x2"])
                )
                for i in self.__floads
            ]
        ) - sum(
            [
                i["z"]
                if i["x1"] == i["x2"]
                else integrate(i["z"], (self.__x, i["x1"], i["x2"]))
                for i in self.__mloads
            ]
        )
        self.__MxN = -sum(
            i["x"]
            if i["x1"] == i["x2"]
            else integrate(i["x"], (self.__x, i["x1"], i["x2"]))
            for i in self.__mloads
        )
        if self.__xroller is not None:
            self.__Ny2 = self.__MzN / (self.__xroller - self.__xpin)
            self.__Ny1 = self.__Ny - self.__Ny2

    def __Mechanical_analaysis(self) -> None:
        # fxw
        self.__fxw = -integrate(
            sum(
                [self.__Nx * SingularityFunction(self.__x, self.__xpin, -1)]
                + [
                    i["x"] * SingularityFunction(self.__x, i["x1"], -1)
                    if i["x1"] == i["x2"]
                    else i["x"]
                    * (
                        SingularityFunction(self.__x, i["x1"], 0)
                        - SingularityFunction(self.__x, i["x2"], 0)
                    )
                    for i in self.__floads
                ]
            ),
            self.__x,
        )
        # fyw
        self.__fyw = sum(
            [
                -i["y"] * SingularityFunction(self.__x, i["x1"], -1)
                if i["x1"] == i["x2"]
                else -i["y"]
                * (
                    SingularityFunction(self.__x, i["x1"], 0)
                    - SingularityFunction(self.__x, i["x2"], 0)
                )
                for i in self.__floads
            ]
            + [
                i["z"] * SingularityFunction(self.__x, i["x1"], -2)
                # if i["x1"] == i["x2"]
                # else i["z"]
                # * (
                #     SingularityFunction(self.__x, i["x1"], -1)
                #     - SingularityFunction(self.__x, i["x2"], -1)
                # )
                for i in self.__mloads
            ]
            + (
                [
                    -self.__Ny * SingularityFunction(self.__x, self.__xpin, -1),
                    self.__MzN * SingularityFunction(self.__x, self.__xpin, -2),
                ]
                if self.__xroller is None
                else [
                    -self.__Ny1 * SingularityFunction(self.__x, self.__xpin, -1),
                    -self.__Ny2 * SingularityFunction(self.__x, self.__xroller, -1),
                ]
            )
        )
        # shear force
        self.__v = -integrate(self.__fyw, self.__x)
        # bending moment
        self.__Mz = integrate(
            self.__v
            - sum(
                [
                    i["z"]
                    * (
                        SingularityFunction(self.__x, i["x1"], 0)
                        - SingularityFunction(self.__x, i["x2"], 0)
                    )
                    for i in self.__mloads
                ]
            ),
            self.__x,
        )
        # torque
        self.__Mx = -integrate(
            sum(
                [self.__MxN * SingularityFunction(self.__x, self.__xpin, -1)]
                + [
                    i["x"] * SingularityFunction(self.__x, i["x1"], -1)
                    if i["x1"] == i["x2"]
                    else i["x"]
                    * (
                        SingularityFunction(self.__x, i["x1"], 0)
                        - SingularityFunction(self.__x, i["x2"], 0)
                    )
                    for i in self.__mloads
                ]
            ),
            self.__x,
        )
        # tau_y_max stress
        self.__tauy = self.__Mx * (
            1 / self.__C1W / self.__WT / self.__W**2
            + 1 / self.__C1F / self.__FT / self.__F**2
        )
        # normal stress
        self.__sigma = self.__fxw / self.__Area - self.__Mz * self.__ymax / self.__Izz
        # tau_xy_max stress
        self.__tauxy = (
            self.__v * self.__WT * self.__ybar**2 / 2 / self.__Iyy / self.__WT
        )

    def loadings(self):
        """
        return all loading entries in plot
        """
        fig1, ax1 = plt.subplots(2, 1)
        fig2, ax2 = plt.subplots(2, 1)

        ax1[0].set(title="Moment Loadings", ylabel=r"$M_{x}$")
        ax1[1].set(xlabel=r"$x$", ylabel=r"$M_{z}$")
        ax2[0].set(title="Force Loadings", ylabel=r"$F_{x}$")
        ax2[1].set(xlabel=r"$x$", ylabel=r"$F_{y}$")
        for i in self.__mloads:
            if i["x1"] == i["x2"]:
                ax1[0].vlines(i["x1"], 0, i["x"], color="red")
                ax1[1].vlines(i["x1"], 0, i["z"], color="orange")
            else:
                ax1[0].plot(
                    np.linspace(i["x1"], i["x2"]),
                    [i["x"].subs(self.__x, j) for j in np.linspace(i["x1"], i["x2"])],
                    color="red",
                )
                ax1[1].plot(
                    np.linspace(i["x1"], i["x2"]),
                    [i["z"].subs(self.__x, j) for j in np.linspace(i["x1"], i["x2"])],
                    color="orange",
                )
        for i in self.__floads:
            if i["x1"] == i["x2"]:
                ax2[0].vlines(i["x1"], 0, i["x"], color="blue")
                ax2[1].vlines(i["x1"], 0, i["y"], color="green")
            else:
                ax2[0].plot(
                    np.linspace(i["x1"], i["x2"]),
                    [i["x"].subs(self.__x, j) for j in np.linspace(i["x1"], i["x2"])],
                    color="blue",
                )
                ax2[1].plot(
                    np.linspace(i["x1"], i["x2"]),
                    [i["y"].subs(self.__x, j) for j in np.linspace(i["x1"], i["x2"])],
                    color="green",
                )
        return (fig1, fig2)

    def beam_geom(self):
        """
        return beam geometry parameters
        """
        return {
            "Izz": latex(self.__Izz),
            "Iyy": latex(self.__Iyy),
            "ybar": latex(self.__ybar),
            "ymax": latex(self.__ymax),
        }

    def calculate(self) -> bool:
        """
        solve the beam
        """
        self.__statical_analysis()
        self.__Mechanical_analaysis()
        return True

    def reactions(self) -> dict:
        """
        return reaction forces and moments
        """
        if self.__xroller is None:
            return {
                "Nx": self.__Nx,
                "Ny": self.__Ny,
                "Mz": self.__MzN,
                "Mx": self.__MxN,
            }
        return {
            "Nx_pin": self.__Nx,
            "Ny_pin": self.__Ny1,
            "N_roller": self.__Ny2,
            "Mx": self.__MxN,
        }

    def bending(self) -> dict:
        """
        return w(x), V(x), M(x) in latex
        """
        return {"w": latex(self.__fyw), "V": latex(self.__v), "M": latex(self.__Mz)}

    def bending_plot(self):
        """
        return fig of V(x) and M(x)
        """
        fig, ax = plt.subplots(2, 1)
        ax[0].set(title="Shear Force and Bending Moment", ylabel="V")
        ax[1].set(xlabel="x", ylabel="M")
        ax[0].plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__v.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        ax[1].plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__Mz.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        return fig

    def torque(self):
        """
        return M_x(x) in latex
        """
        return latex(self.__Mx)

    def torqe_plot(self):
        """
        return fig of T(x)
        """
        fig, ax = plt.subplots()
        ax.set(title="Torque", ylabel=r"$M_{x}(x)$")
        ax.plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__Mx.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        return fig

    def tau_y_max(self):
        """
        return tau_y_max(x) in latex
        """
        return latex(self.__tauy)

    def tau_y_max_plot(self):
        """
        return fig of tau_y_max(x)
        """
        fig, ax = plt.subplots()
        ax.set(title=r"$\tau_{y,max}$", ylabel=r"$\tau_{y,max}(x)$")
        ax.plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__tauy.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        return fig

    def normal_stress_max(self):
        """
        return max sigma(x) in latex
        """
        return latex(self.__sigma)

    def normal_stress_max_plot(self):
        """
        return fig of max sigma(x)
        """
        fig, ax = plt.subplots()
        ax.set(title=r"$\sigma_{x,max}$", ylabel=r"$\sigma_{x,max}(x)$")
        ax.plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__sigma.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        return fig

    def tau_xy_max(self):
        """
        return tau_xy_max(x) in latex
        """
        return latex(self.__tauxy)

    def tau_xy_max_plot(self):
        """
        return fig of tau_xy_max(x)
        """
        fig, ax = plt.subplots()
        ax.set(title=r"$\tau_{xy,max}$", ylabel=r"$\tau_{xy,max}(x)$")
        ax.plot(
            np.linspace(0, self.__lenght * 0.99, 100),
            [
                self.__tauxy.subs(self.__x, i)
                for i in np.linspace(0, self.__lenght * 0.99, 100)
            ],
        )
        return fig


if __name__ == "__main__":
    pass
