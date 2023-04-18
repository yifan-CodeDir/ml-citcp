library(scmamp)
data<-read.csv('/Users/xxxx/Documents/ml-citcp/result/RQ1/rapfd_record.csv',check.names=FALSE) # read data
# non-parametric ANOVA analysis, Friedman test with the Iman and Davemport extension
imanDavenportTest(data = data)
# Friedman post hoc test corrected by Bergmann and Hommel’s procedure
raw.pvalues <- postHocTest(data = data, use.rank = T, control = NULL, test = 'friedman', correct = 'shaffer')

# plot p-values using Critical difference
p1 <- plotRanking(pvalues = raw.pvalues$corrected.pval, 
            summary = raw.pvalues$summary, 
            alpha=0.05)
# plot using matrix
# plotPvalues(pvalue.matrix = raw.pvalues$corrected.pval, 
#            alg.order = NULL, show.pvalue = TRUE, 
#            font.size = 5)

# dev.off()
