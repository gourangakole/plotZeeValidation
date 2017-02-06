import ROOT
import array, sys
from optparse import OptionParser

hmcCorr = []
hmc = []
hdata = []
                
transfName   = ["trasfheedown","trasfheeup","trasfhebdown","trasfhebup"]
plotNameData = ["hidmvadataeedown","hidmvadataeeup","hidmvadataebdown","hidmvadataebup"]
plotNameMC   = ["hidmvamceedown","hidmvamceeup","hidmvamcebdown","hidmvamcebup"]
plotDef      = [(10000, -1.0, 1.0), (10000, -1.0, 1.0), (10000, -1.0, 1.0), (10000, -1.0, 1.0)]

def test(makeOutput=False):
    graphs = []
    trans = ""
    
    if (not makeOutput):
        trans = ROOT.TFile("transformationIDMVA.root")
        for t in transfName:
            graphs.append(trans.Get(t))
        
    if (len(plotNameMC) != len(plotNameData)):
        print "You need same number of plots for data and MC"
        sys.exit(1)

    for histoList, plotNames, suffix in (
        (hdata,   plotNameData, ""),
        (hmc,     plotNameMC,   ""),
        (hmcCorr, plotNameMC,   "_corr"),
        ):
        
        for z in xrange(len(plotNames)):

            title = plotNames[z]
            if title.startswith('h'):
                title = title[1:]

            histoList.append(ROOT.TH1F(plotNames[z] + suffix, title, plotDef[z][0], plotDef[z][1], plotDef[z][2]))

    filenames = [sys.argv[-2], sys.argv[-1]]
    for nf, f in enumerate(filenames):

        print "processing",f

        fin = ROOT.TFile(f)
        t = fin.Get("diphotonDumper/trees/zeevalidation_13TeV_All")

        et1 = array.array('f', [0])
        eta1 = array.array('f', [0])
        s41 = array.array('f', [0])
        etawidth1 = array.array('f', [0])
        full5x5r91 = array.array('f', [0])
        et2 = array.array('f', [0])
        eta2 = array.array('f', [0])
        s42 = array.array('f', [0])
        etawidth2 = array.array('f', [0])
        full5x5r92 = array.array('f', [0])
     
        idmvaup1 = array.array('f', [0])
        idmvadown1 = array.array('f', [0])
        idmvaup2 = array.array('f', [0])
        idmvadown2 = array.array('f', [0])

        weight = array.array('f', [0])
        mass = array.array('f', [0])

        t.SetBranchStatus("*", 0)
        t.SetBranchStatus("leadPt", 1)
        t.SetBranchStatus("leadEta", 1)
        t.SetBranchStatus("leads4ratio", 1)
        t.SetBranchStatus("leadetawidth", 1)
        t.SetBranchStatus("leadfull5x5r9", 1)
        t.SetBranchStatus("leadIDMVA", 1)
        t.SetBranchStatus("subleadPt", 1)
        t.SetBranchStatus("subleadEta", 1)
        t.SetBranchStatus("subleads4ratio", 1)
        t.SetBranchStatus("subleadetawidth", 1)
        t.SetBranchStatus("subleadfull5x5r9", 1)
        t.SetBranchStatus("subIDMVA", 1)
        t.SetBranchStatus("weight", 1)
        t.SetBranchStatus("mass", 1)

        t.SetBranchAddress("leadPt", et1)
        t.SetBranchAddress("leadEta", eta1)
        t.SetBranchAddress("leads4ratio", s41)
        t.SetBranchAddress("leadetawidth", etawidth1)
        t.SetBranchAddress("leadfull5x5r9", full5x5r91)
        t.SetBranchAddress("leadIDMVA", idmvaup1)
        t.SetBranchAddress("leadIDMVA", idmvadown1)
        t.SetBranchAddress("subleadPt", et2)
        t.SetBranchAddress("subleadEta", eta2)
        t.SetBranchAddress("subleads4ratio", s42)
        t.SetBranchAddress("subleadetawidth", etawidth2)
        t.SetBranchAddress("subleadfull5x5r9", full5x5r92)
        t.SetBranchAddress("subIDMVA", idmvaup2)
        t.SetBranchAddress("subIDMVA", idmvadown2)
        t.SetBranchAddress("weight", weight)
        t.SetBranchAddress("mass", mass)

        entries = t.GetEntries()

        for z in xrange(entries):
            if (z+1) % 5000 == 0:
               print "processing entry %d/%d (%5.1f%%)\r" % (z + 1, entries, (z+1) / float(entries) * 100.),
               sys.stdout.flush()

            t.GetEntry(z)
            
            if (mass[0] < 70. or mass[0] > 110.):
                continue
                
            if (et1[0] > 15.):
                if (nf == 0):
                    if (abs(eta1[0])<1.5):
                        hmc[2].Fill(idmvadown1[0]-0.005, weight[0])
                        hmc[3].Fill(idmvadown1[0]+0.005, weight[0])
                        if (not makeOutput):
                            hmcCorr[2].Fill(graphs[2].Eval(idmvadown1[0]-0.005, weight[0]))
                            hmcCorr[3].Fill(graphs[3].Eval(idmvadown1[0]+0.005, weight[0]))
                    else:
                        hmc[0].Fill(idmvadown1[0]-0.005, weight[0])
                        hmc[1].Fill(idmvadown1[0]+0.005, weight[0])
                        if (not makeOutput):
                            hmcCorr[0].Fill(graphs[0].Eval(idmvadown1[0]-0.005, weight[0]))
                            hmcCorr[1].Fill(graphs[1].Eval(idmvadown1[0]+0.005, weight[0]))
                else:
                    if (abs(eta1[0])<1.5):
                        hdata[2].Fill(idmvadown1[0]-0.005, weight[0])
                        hdata[3].Fill(idmvadown1[0]+0.005, weight[0])
                    else:
                        hdata[0].Fill(idmvadown1[0]-0.005, weight[0])
                        hdata[1].Fill(idmvadown1[0]+0.005, weight[0])
                        
            if (et2[0] > 15.):
                if (nf == 0):
                    if (abs(eta2[0])<1.5):
                        hmc[2].Fill(idmvadown2[0]-0.005, weight[0])
                        hmc[3].Fill(idmvadown2[0]+0.005, weight[0])
                        if (not makeOutput):
                            hmcCorr[2].Fill(graphs[2].Eval(idmvadown2[0]-0.005, weight[0]))
                            hmcCorr[3].Fill(graphs[3].Eval(idmvadown2[0]+0.005, weight[0]))
                    else:
                        hmc[0].Fill(idmvadown2[0]-0.005, weight[0])
                        hmc[1].Fill(idmvadown2[0]+0.005, weight[0])
                        if (not makeOutput):
                            hmcCorr[0].Fill(graphs[0].Eval(idmvadown2[0]-0.005, weight[0]))
                            hmcCorr[1].Fill(graphs[1].Eval(idmvadown2[0]+0.005, weight[0]))
                else:
                    if (abs(eta2[0])<1.5):
                        hdata[2].Fill(idmvadown2[0]-0.005, weight[0])
                        hdata[3].Fill(idmvadown2[0]+0.005, weight[0])
                    else:
                        hdata[0].Fill(idmvadown2[0]-0.005, weight[0])
                        hdata[1].Fill(idmvadown2[0]+0.005, weight[0])

        print                
        # end of loop over tree entries
    # end of loop over input files

                
    if (not makeOutput):
        c = []
        for i in xrange(len(hmc)):
            c.append(ROOT.TCanvas("c"+str(i), ""))
            hmc[i].Scale(hdata[i].Integral()/hmc[i].Integral())
            hmcCorr[i].Scale(hdata[i].Integral()/hmcCorr[i].Integral())
            hmc[i].Draw("HIST")
            hmc[i].SetLineColor(ROOT.kRed)
            hmcCorr[i].Draw("SAMEHIST")
            hmcCorr[i].SetLineColor(ROOT.kBlue)
            hdata[i].Draw("SAMEPE")
            hdata[i].SetMarkerStyle(20)

        print "plotting done, press enter to continue"
        raw_input()
    else:
        output = ROOT.TFile("inputHistos.root", "recreate")
        for i, h in enumerate(hmc):
            hmc[i].Scale(hdata[i].Integral()/hmc[i].Integral())
            h.Write()
        for h in hdata:
            h.Write()
        output.Close()
        print "wrote inputHistos.root"

def makeTransformation():
    global hmc, hdata, transfName, plotNameData, plotNameMC, plotDef      

    f = ROOT.TFile("inputHistos.root")
    for p in plotNameData:
        hdata.append(f.Get(p))

    for p in plotNameMC:              
        hmc.append(f.Get(p))

    if (len(plotNameMC) != len(plotNameData)):
        print "You need same number of plots for data and MC"
        sys.exit(1)

    graphs = []
    for z in xrange(len(hmc)):
        # NORMALIZE MC TO DATA
        hmc[z].Scale(hdata[z].Integral()/hmc[z].Integral())
        hcdfmc = hmc[z].GetCumulative()
        hcdfmc.Scale(1./hmc[z].Integral())
        
        # Make general
        uniform = ROOT.TH1F("uniform"+str(z), "", plotDef[z][0], plotDef[z][1], plotDef[z][2])
        for i in xrange(plotDef[z][0]):
            uniform.SetBinContent(i, 10) 

        uniform.Scale(hdata[z].Integral()/uniform.Integral())
        uniformcdf = uniform.GetCumulative()
        uniformcdf.Scale(1./hmc[z].Integral())

        xt = array.array('d', [x*0.001 for x in xrange(10000)])
        yt = array.array('d', [x*0.001 for x in xrange(10000)])

        xyxy = array.array('d', [x for x in xrange(10000)]) #important 1000 bins in important because this has to match with the original histogram
        
        # xx = array('d',[ x in xrange(1000)])
        # xyxy = array.array('i', [0,1,2,3,4])
        print "len(xyxy)", len(xyxy)

        hmc[z].GetQuantiles(len(yt), xt, yt) # xt MC qualties 

        # print "xt", xt

        hcdfdata = hdata[z].GetCumulative()
        hcdfdata.Scale(1./hdata[z].Integral())

        xdatat = array.array('d', [x*0.001 for x in xrange(10000)])
        ydatat = array.array('d', [x*0.001 for x in xrange(10000)])
        # debug for IDMVA
        # print "before calculation: xdatat", xdatat, "ydatat", ydatat
        hdata[z].GetQuantiles(len(ydatat), xdatat, ydatat) #xdata Data qualties
        # print "after calculation: xdatat", xdatat, "ydatat", ydatat
        # print "debug1"
        # print "x", x

        # print "transfName[z]", transfName[z], "len(ydatat)", len(ydatat) , "xt", xt
        
        graphs.append(ROOT.TGraph(len(xt), xyxy, xt)) # TGraph is filled by (n, range_0_1000, xrange_of_variables)
        graphs[-1].SetName(transfName[z])

    out = ROOT.TFile("transformation_IDMVA.root", "recreate")
    for g in graphs:
        g.Write()
    out.Close()
    print "wrote transformation.root"

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
