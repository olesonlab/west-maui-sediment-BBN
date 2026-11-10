"""Environmental Management figure settings: 174 mm wide (full page width), Liberation Sans
(metric-compatible with Arial), lettering 8-12 pt, fonts embedded. save() writes vector PDF and EPS
plus 600 dpi PNG and TIFF (RGB, LZW) at the exact final size."""
import matplotlib as mpl
from PIL import Image
W = 174 / 25.4  # inches

def setup(size=8):
    mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": size, "axes.unicode_minus": True,
                         "pdf.fonttype": 42, "ps.fonttype": 42, "legend.fontsize": size,
                         "legend.title_fontsize": size, "xtick.labelsize": size, "ytick.labelsize": size,
                         "axes.labelsize": size})

def save(fig, out, dpi=600):
    fig.savefig(out + ".pdf"); fig.savefig(out + ".eps")
    fig.savefig(out + ".png", dpi=dpi)
    Image.open(out + ".png").convert("RGB").save(out + ".tif", dpi=(dpi, dpi), compression="tiff_lzw")
