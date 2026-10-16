# Figure 6: bank erosion by major landowner under select management alternatives.
#
# Stacked bars of modeled bank erosion (tonnes/yr) for each landowner, with each
# segment labelled by that landowner's percent change from its own baseline.
#
# Based on Whitney Goodell's ggplot2 script (2023-06-27; edited by K. Oleson,
# 2026-03-14). In the earlier version the percentages were typed onto the
# exported PDF by hand; here they are computed from the data and drawn by R.
#
# Data: sheet "Landowner_analysis" of data/Results-scenario-landowner-subwatershed.xlsx
# (the same values as forR_erosion_byLO_WG.csv used for the original figure).
# R_200 uses the row marked "(ORIGINAL)", which the original figure plotted.
#
# Run from the repository root:  Rscript code/fig6_landowner.R
# Requires: ggplot2, readxl

suppressPackageStartupMessages({
  library(ggplot2)
  library(readxl)
})

args <- commandArgs(trailingOnly = FALSE)
script <- sub("^--file=", "", args[grep("^--file=", args)])
root <- if (length(script)) normalizePath(file.path(dirname(script), "..")) else getwd()

raw <- read_excel(file.path(root, "data", "Results-scenario-landowner-subwatershed.xlsx"),
                  sheet = "Landowner_analysis", col_names = FALSE, range = "A1:M17",
                  .name_repair = "minimal")
raw <- as.data.frame(raw)

# Spreadsheet rows used (1-based) and the labels used in the paper
rows <- c(Baseline = 4, R_200 = 11, VH_T = 12, H_T = 15, VH_A = 14, H_A = 17)
# Erosion (tonnes/yr) columns: G = Maui Land & Pine, I = Kaanapali, K = State, M = Other
cols <- c(MLP = 7, KLMC = 9, State = 11, Other = 13)

vals <- sapply(cols, function(j) as.numeric(raw[rows, j]))
rownames(vals) <- names(rows)

owners <- c(KLMC = "Ka\u02BBanapali Land Mgt Co", MLP = "Maui Land & Pine",
            Other = "Other", State = "State government")
fills  <- c(KLMC = "tan4", MLP = "gold2", Other = "beige", State = "royalblue1")
text_col <- c(KLMC = "white", MLP = "black", Other = "black", State = "white")

d <- do.call(rbind, lapply(names(owners), function(o) {
  data.frame(Scenario = rownames(vals), owner = o, tonnes = vals[, o],
             pct = 100 * (vals[, o] / vals["Baseline", o] - 1))
}))
d$Scenario <- factor(d$Scenario, levels = names(rows))
d$owner <- factor(d$owner, levels = names(owners))   # first level stacks on top
d$label <- ifelse(d$Scenario == "Baseline", "",
                  ifelse(round(d$pct) == 0, "0%", sprintf("%.0f%%", d$pct)))

write.csv(d[, c("Scenario", "owner", "tonnes", "pct")],
          file.path(root, "code", "fig6_values.csv"), row.names = FALSE)

p <- ggplot(d, aes(x = Scenario, y = tonnes, fill = owner)) +
  geom_col(width = 0.8) +
  geom_text(aes(label = label, colour = owner),
            position = position_stack(vjust = 0.5), size = 3, show.legend = FALSE) +
  scale_fill_manual(values = fills, labels = owners, name = NULL) +
  scale_colour_manual(values = text_col, guide = "none") +
  scale_y_continuous(expand = expansion(mult = c(0, 0.03))) +
  labs(x = "Scenario", y = "Erosion under each scenario (tonnes/yr)") +
  theme_minimal(base_size = 11) +
  theme(legend.position = "right",
        legend.text = element_text(size = 8),
        axis.title.x = element_text(margin = margin(t = 10)),
        axis.title.y = element_text(margin = margin(r = 10)),
        panel.grid.major.x = element_blank(),
        plot.margin = margin(10, 5, 5, 10))

out <- file.path(root, "figures")
ggsave(file.path(out, "Figure6_landowner.pdf"), p, width = 7, height = 5.5, device = cairo_pdf)
ggsave(file.path(out, "Figure6_landowner.png"), p, width = 7, height = 5.5, dpi = 300, bg = "white")
cat("Figure 6 written to", out, "\n")
print(d[d$Scenario != "Baseline", c("Scenario", "owner", "tonnes", "label")], row.names = FALSE)
