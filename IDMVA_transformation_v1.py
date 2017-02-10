import ROOT
import array, sys
from optparse import OptionParser

hmcCorr = []
hmc = []
hdata = []

hvariation = []
hnominal = []
           
transfName   = ["trasfheedown","trasfheeup","trasfhebdown","trasfhebup"]
plotNameNominal = ["idmva_cat1_DYToEE","idmva_cat1_DYToEE","idmva_cat0_DYToEE","idmva_cat0_DYToEE"]
plotNameVariation   = ["idmva_cat1_DYToEE_bottom","idmva_cat1_DYToEE_top","idmva_cat0_DYToEE_bottom","idmva_cat0_DYToEE_top"]
plotDef      = [(100, -1.0, 1.0), (100, -1.0, 1.0), (100, -1.0, 1.0), (100, -1.0, 1.0)]


def makeTransformation():
    global hvariation, hnominal, transfName, plotNameData, plotNameMC, plotDef      

    f = ROOT.TFile("inputHistosIDMVA.root")
    for p in plotNameNominal:
        hnominal.append(f.Get(p))

    for p in plotNameVariation:              
        hvariation.append(f.Get(p))

    if (len(plotNameVariation) != len(plotNameNominal)):
        print "You need same number of plots for nominal and variation"
        sys.exit(1)

    graphs = []
    for z in xrange(len(hnominal)):
        # NORMALIZE nominal TO variation
        hnominal[z].Scale(hvariation[z].Integral()/hnominal[z].Integral())
        hcdfnominal = hnominal[z].GetCumulative()
        hcdfnominal.Scale(1./hnominal[z].Integral())
        
        # Make general
        uniform = ROOT.TH1F("uniform"+str(z), "", plotDef[z][0], plotDef[z][1], plotDef[z][2])
        for i in xrange(plotDef[z][0]):
            uniform.SetBinContent(i, 10) 
        
        uniform.Scale(hvariation[z].Integral()/uniform.Integral())
        uniformcdf = uniform.GetCumulative()
        uniformcdf.Scale(1./hnominal[z].Integral())

        xnominalt = array.array('d', [x*0.001 for x in xrange(1000)])
        ynominalt = array.array('d', [x*0.001 for x in xrange(1000)])
        
        hnominal[z].GetQuantiles(len(ynominalt), xnominalt, ynominalt)

        hcdfvariation = hvariation[z].GetCumulative()
        hcdfvariation.Scale(1./hvariation[z].Integral())
        
        xvariationt = array.array('d', [x*0.001 for x in xrange(1000)])
        yvariationt = array.array('d', [x*0.001 for x in xrange(1000)])
        hvariation[z].GetQuantiles(len(yvariationt), xvariationt, yvariationt)

        graphs.append(ROOT.TGraph(len(xnominalt), xnominalt, xvariationt))


        # graphs.append(ROOT.TGraph(len(xt), xyxy, xt)) # decide what to put
        graphs[-1].SetName(transfName[z])

    out = ROOT.TFile("transformation_IDMVA_Moriond17_v1.root", "recreate")
    for g in graphs:
        g.Write()
    out.Close()
    print "wrote transformation_IDMVA_Moriond17_v1.root"

if (__name__ == "__main__"):
    parser = OptionParser(usage="Usage: %prog [options] [mc_ntuple_filename] [target_ntuple_filename]",)
    parser.add_option("-p", "--prepare-plots", dest="preparePlots", action="store_true", help="Dump plots", default=False)
    parser.add_option("-c", "--transform", action="store_true", help="Derive actual transformations", default=False)
    parser.add_option("-t", "--test", action="store_true", help="Test transformations", default=False)
    # parser.add_option(

    (options, arg) = parser.parse_args()

    if (options.preparePlots):
        print "Preparing necessary plots..."
        test(True)   
        print "Done."
        sys.exit(0)
    elif (options.transform): 
        print "Deriving transformations..."
        makeTransformation()
        print "Done."
        sys.exit(0)
    elif (options.test): 
        print "Testing..."
        test(False)
        print "Done."
        sys.exit(0)
