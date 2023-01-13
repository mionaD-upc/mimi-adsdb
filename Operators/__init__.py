import landing
import formatted
import trusted
import explotation 
import feature_generation
import modelling
import feature_selection

if __name__ == '__main__':
    landing.main()
    formatted.main()
    trusted.main()
    explotation.main()
    df = feature_generation.main()
    modelling.main1()

    print("Do you want to execute Feature Selection? (30min) y/n")
    boption = input("")
    feature_selection.main() if boption.strip() == 'y' else None
    
    modelling.main2(df)
    print('\nEND OF THE PROGRAM')
    
    
