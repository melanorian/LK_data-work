#!/usr/bin/env Rscript

library(tidyverse)

# ---------------- CONFIGURATION ----------------
base_dir <- "/home/melanie/Documents/LK_data/LK_inventory_report"

input_file <- file.path(
  base_dir,
  "8_summarized_inventory_with_duplicates_L5.csv"
)

out_dir <- file.path(base_dir, "visualisation")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
# ----------------------------------------------


# ---------------- LOAD DATA ----------------
df <- read_csv(input_file, show_col_types = FALSE)

# Ensure factors are clean
df <- df %>%
  mutate(
    released = factor(released, levels = c(0, 1)),
    release_version = as.factor(release_version),
    data_domain = as.factor(data_domain),
    processing_level = as.factor(processing_level)
  )


# =========================================================
# 1. PIE CHART: released vs not released vs DR1 vs DR2
# =========================================================

df_release <- df %>%
  mutate(release_group = case_when(
    released == 0 ~ "Not released",
    release_version == "DR1" ~ "DR1",
    release_version == "DR2" ~ "DR2",
    TRUE ~ "Other"
  )) %>%
  group_by(release_group) %>%
  summarise(size = sum(collection_size_bytes, na.rm = TRUE))

p_release <- ggplot(df_release, aes(x = "", y = size, fill = release_group)) +
  geom_col(width = 1) +
  coord_polar("y") +
  theme_void() +
  labs(title = "Storage by release status")

ggsave(file.path(out_dir, "pie_release_status.svg"), p_release, device = "svg")


# =========================================================
# 2. PIE CHART: all data by domain (including special category)
# =========================================================

df_domain <- df %>%
  mutate(domain = coalesce(data_domain, "unknown")) %>%
  group_by(domain) %>%
  summarise(size = sum(collection_size_bytes, na.rm = TRUE))

p_domain <- ggplot(df_domain, aes(x = "", y = size, fill = domain)) +
  geom_col(width = 1) +
  coord_polar("y") +
  theme_void() +
  labs(title = "Storage by data domain")

ggsave(file.path(out_dir, "pie_domain_all.svg"), p_domain, device = "svg")


# =========================================================
# 3. PIE CHART: processing level (all data)
# =========================================================

df_proc <- df %>%
  group_by(processing_level) %>%
  summarise(size = sum(collection_size_bytes, na.rm = TRUE))

p_proc <- ggplot(df_proc, aes(x = "", y = size, fill = processing_level)) +
  geom_col(width = 1) +
  coord_polar("y") +
  theme_void() +
  labs(title = "Storage by processing level")

ggsave(file.path(out_dir, "pie_processing_level.svg"), p_proc, device = "svg")


# =========================================================
# 4. STACKED BAR: processing level per data domain
# =========================================================

df_bar <- df %>%
  group_by(data_domain, processing_level) %>%
  summarise(size = sum(collection_size_bytes, na.rm = TRUE), .groups = "drop")

p_bar <- ggplot(df_bar, aes(x = data_domain, y = size, fill = processing_level)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Processing level per data domain",
    x = "Data domain",
    y = "Size (bytes)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(file.path(out_dir, "stacked_processing_by_domain.svg"), p_bar, device = "svg")